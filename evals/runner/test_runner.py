"""Contract test for the live skill invocation path, without API credentials."""

import base64
import io
import unittest
import zipfile
from types import SimpleNamespace

from evals.runner.runner import invoke_subject, skill_zip


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


if __name__ == "__main__":
    unittest.main()
