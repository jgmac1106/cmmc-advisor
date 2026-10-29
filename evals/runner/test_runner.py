"""Contract test for the live skill invocation path, without API credentials."""

import base64
import io
import json
import re
import unittest
import zipfile
from types import SimpleNamespace

from evals.runner.runner import REPO_ROOT, SKILL_DIR, invoke_subject, load_scenario, skill_zip
from evals.runner.precheck import m365_classification_candidates, run_precheck


class FakeContainers:
    def __init__(self):
        self.created = None
        self.deleted = None

    def create(self, **kwargs):
        self.created = kwargs
        return SimpleNamespace(id="cntr_test")

    def delete(self, container_id):
        self.deleted = container_id


class FakeResponses:
    def __init__(self):
        self.created = None

    def create(self, **kwargs):
        self.created = kwargs
        return SimpleNamespace(
            output_text="contract-specific answer",
            output=[SimpleNamespace(type="shell_call", action={
                "commands": ["cat /mnt/data/skills/cmmc-advisor/SKILL.md"]
            })],
        )


class RunnerContractTest(unittest.TestCase):
    def test_inline_bundle_and_mounted_skill_are_used(self):
        client = SimpleNamespace(containers=FakeContainers(), responses=FakeResponses())
        answer, skill_read = invoke_subject(
            client, {"id": "sample", "prompt": "What level applies?"},
            "gpt-6-astra", skill_zip(),
        )
        self.assertEqual(answer, "contract-specific answer")
        self.assertTrue(skill_read)
        self.assertEqual(client.containers.deleted, "cntr_test")
        inline = client.containers.created["skills"][0]
        self.assertEqual(inline["type"], "inline")
        with zipfile.ZipFile(io.BytesIO(base64.b64decode(inline["source"]["data"]))) as zf:
            self.assertIn("cmmc-advisor/SKILL.md", zf.namelist())
            self.assertIn("cmmc-advisor/references/domains/ac-access-control.md", zf.namelist())
            self.assertIn("cmmc-advisor/LICENSE", zf.namelist())
        call = client.responses.created
        self.assertEqual(call["tools"][0]["environment"]["container_id"], "cntr_test")
        self.assertEqual(call["tools"][1]["type"], "web_search")
        self.assertEqual(call["tool_choice"], "required")
        self.assertIn("What level applies?", call["input"])

    def test_container_deleted_when_response_fails(self):
        client = SimpleNamespace(containers=FakeContainers(), responses=FakeResponses())
        def fail(**kwargs):
            raise RuntimeError("API error")
        client.responses.create = fail
        with self.assertRaisesRegex(RuntimeError, "API error"):
            invoke_subject(client, {"id": "sample", "prompt": "Question"},
                           "gpt-6-astra", skill_zip())
        self.assertEqual(client.containers.deleted, "cntr_test")


class MicrosoftAuthorizationRegressionTest(unittest.TestCase):
    def test_obsolete_classification_candidates(self):
        examples = {
            "GCC is FedRAMP Moderate plus DoD IL2.": "gcc_blanket_moderate",
            "**GCC** is only FedRAMP\nModerate.": "gcc_blanket_moderate",
            "GCC High is FedRAMP High plus DoD IL5.": "gcc_high_blanket_il5",
            "GCC High holds IL5 provisional authorization.": "gcc_high_blanket_il5",
            "GCC High holds a FedRAMP High JAB P-ATO.": "gcc_high_jab",
            "GCC High package (MSO365MT).": "gcc_high_wrong_package",
            "IL5 for the productivity plane requires Microsoft 365 GCC High.": "il5_default_gcc_high",
        }
        for answer, expected in examples.items():
            with self.subTest(answer=answer):
                self.assertIn(expected, m365_classification_candidates(answer))
                self.assertIn(expected, run_precheck(answer, {})["m365_classification_candidates"])

    def test_source_separated_and_other_vendor_claims_are_not_flagged(self):
        for answer in (
            "Microsoft describes GCC as supporting High; MSO365MT's Marketplace profile is Class C (Moderate). Resolve the difference with package evidence.",
            "GCC High can demonstrate IL4 equivalency per Microsoft, not a verified IL5 PA.",
            "Office 365 DoD is described as IL5; check eligibility and service authorization.",
            "ServiceNow GCC is FedRAMP High. Azure Government has separate IL5 service scope.",
            "MSO365MT is GCC; FR1824057433 is GCC High, Agency path.",
        ):
            with self.subTest(answer=answer):
                self.assertEqual([], m365_classification_candidates(answer))

    def test_quoted_or_rejected_candidates_remain_advisory(self):
        answer = 'Reject the claim "GCC High holds IL5"; verify the exact service PA.'
        result = run_precheck(answer, {})
        self.assertIn("gcc_high_blanket_il5", result["m365_classification_candidates"])
        self.assertEqual([], result["hard_fail_flags"])

    def test_snapshot_retains_source_identity_and_partial_refresh_dates(self):
        data = json.loads((SKILL_DIR / "references/data/fedramp-snapshot.json").read_text())
        self.assertEqual("1.1", data["schema_version"])
        self.assertEqual("2026-04-21", data["verification_date"])
        self.assertEqual("2026-10-29", data["last_updated"])
        vendors = {item["id"]: item for item in data["vendors"]}
        for name, package, level in (
            ("microsoft-365-gcc", "MSO365MT", "Moderate"),
            ("microsoft-365-gcc-high", "FR1824057433", "High"),
        ):
            with self.subTest(name=name):
                item = vendors[name]
                self.assertEqual(package, item["package_id"])
                self.assertEqual(level, item["fedramp_impact_level"])
                self.assertEqual("Agency ATO", item["authorization_type"])
                self.assertEqual("Agency", item["marketplace_record"]["path"])
                self.assertEqual("FedRAMP Certified", item["marketplace_record"]["status"])
                self.assertTrue(item["primary_source"].endswith(f"/{package}/"))
                self.assertEqual(item["primary_source"], item["marketplace_record"]["url"])
                self.assertEqual("2026-10-29", item["verification_date"])
                self.assertEqual(item["verification_date"], item["marketplace_record"]["access_date"])
                self.assertEqual(item["verification_date"], item["vendor_description"]["access_date"])
                self.assertEqual("FedRAMP High", item["vendor_description"]["fedramp"])
                self.assertTrue(item["vendor_description"]["sources"])
                self.assertEqual([], item["dod_impact_level"])
                self.assertEqual("unverified", item["dod_authorization_verification"]["status"])
                self.assertIn("service-specific", item["cui_suitability"])
                self.assertIn("contract-specific", item["cui_suitability"])
        self.assertIn("unresolved", vendors["microsoft-365-gcc"]["reconciliation_status"])
        self.assertEqual("Entra ID in Azure", vendors["microsoft-365-gcc"]["vendor_description"]["identity_cloud"])
        self.assertEqual("Entra ID in Azure Government", vendors["microsoft-365-gcc-high"]["vendor_description"]["identity_cloud"])
        for item in data["vendors"]:
            if item["id"] not in ("microsoft-365-gcc", "microsoft-365-gcc-high"):
                self.assertNotIn("verification_date", item, "Do not silently redate unreviewed vendors")

    def test_distributed_corpus_has_no_known_obsolete_affirmative_templates(self):
        # These exact historical templates are forbidden even beneath a warning.
        # Avoid a broad GCC+IL5 regex: valid DoD comparisons and quoted corrections
        # must remain possible. Semantic scenarios cover paraphrased errors.
        obsolete = (
            "GCC is FedRAMP Moderate plus DoD IL2",
            "GCC High is FedRAMP High plus DoD IL5",
            "GCC High holds DoD IL2, IL4, and IL5",
            "GCC High holds a FedRAMP High JAB P-ATO under package MSO365MT",
            "GCC High package (MSO365MT)",
            "inherits GCC High FedRAMP High + IL5",
            "GCC Moderate or GCC High",
            "productivity plane requires Microsoft 365 GCC High",
            "requirements must choose M365 GCC High",
            "sovereign tenancy at FedRAMP High plus DoD IL5",
        )
        for path in SKILL_DIR.rglob("*"):
            if path.suffix not in (".md", ".json"):
                continue
            normalized = re.sub(r"\s+", " ", path.read_text().replace("*", ""))
            for phrase in obsolete:
                with self.subTest(path=str(path.relative_to(SKILL_DIR)), phrase=phrase):
                    self.assertNotIn(phrase.lower(), normalized.lower())

    def test_microsoft_scenarios_require_contract_and_service_checks(self):
        scenarios = list((REPO_ROOT / "evals/scenarios").glob("modern-it-m365-*.yaml"))
        self.assertEqual(4, len(scenarios))
        for path in scenarios:
            scenario = load_scenario(path)
            with self.subTest(scenario=scenario["id"]):
                self.assertTrue(scenario["factual_claims_expected"])
                notes = scenario["evaluator_notes"].lower()
                self.assertIn("contract-specific", notes)
                self.assertIn("service-specific", notes)
                self.assertIn("accuracy 0", notes.replace("accuracy (0)", "accuracy 0"))

    def test_bundle_contains_reconciled_data_and_root_routing(self):
        with zipfile.ZipFile(io.BytesIO(skill_zip())) as archive:
            snapshot = json.loads(archive.read("cmmc-advisor/references/data/fedramp-snapshot.json"))
            self.assertEqual("FR1824057433", snapshot["vendors"][1]["package_id"])
            root = archive.read("cmmc-advisor/SKILL.md").decode()
            self.assertIn("references/data/fedramp-snapshot.json", root)
            self.assertIn("contract-specific and service-specific authorization checks", root)
            self.assertIn("Keep vendor descriptions, government", root)


if __name__ == "__main__":
    unittest.main()
