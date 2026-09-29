"""Evaluate the packaged OpenAI skill through the Responses API.

Each scenario gets a fresh hosted container with an inline ZIP built from
skills/cmmc-advisor/. This tests distributed skill files, not a system prompt.
"""

from __future__ import annotations

import argparse
import base64
import io
import json
import os
import sys
import zipfile
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

import yaml

from evals.runner.precheck import run_precheck
from evals.runner.scoring import score_response

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILL_DIR = REPO_ROOT / "skills" / "cmmc-advisor"
DEFAULT_RUBRIC = REPO_ROOT / "evals" / "rubrics" / "cmmc-answer-quality.md"
RESULTS_DIR = REPO_ROOT / "evals" / "results"


def load_scenario(path: Path) -> dict:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not all(data.get(k) for k in ("id", "prompt")):
        raise ValueError(f"{path} must contain nonempty id and prompt")
    return data


def skill_metadata() -> dict:
    text = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    parts = text.split("---", 2)
    if len(parts) < 3 or parts[0].strip():
        raise ValueError("SKILL.md needs YAML frontmatter")
    data = yaml.safe_load(parts[1])
    if not isinstance(data, dict) or data.get("name") != "cmmc-advisor":
        raise ValueError("Expected cmmc-advisor skill metadata")
    if not data.get("description"):
        raise ValueError("Skill description is required")
    return data


def skill_zip() -> bytes:
    """Package the distributed skill folder with one top-level directory."""
    skill_metadata()
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(SKILL_DIR.rglob("*")):
            if path.is_file():
                archive.write(path, f"cmmc-advisor/{path.relative_to(SKILL_DIR)}")
    return buffer.getvalue()


def _skill_read_observed(response) -> bool:
    """Reject a response that did not actually read the mounted skill."""
    for item in response.output:
        if item.type == "shell_call":
            action = item.action.model_dump() if hasattr(item.action, "model_dump") else item.action
            if "SKILL.md" in json.dumps(action):
                return True
    return False


def invoke_subject(client, scenario: dict, model: str, bundle: bytes) -> tuple[str, bool]:
    meta = skill_metadata()
    container = client.containers.create(
        name=f"cmmc-advisor-eval-{scenario['id']}",
        skills=[{
            "type": "inline", "name": meta["name"],
            "description": meta["description"],
            "source": {"type": "base64", "media_type": "application/zip",
                       "data": base64.b64encode(bundle).decode("ascii")},
        }],
    )
    try:
        response = client.responses.create(
            model=model,
            tools=[{"type": "shell", "environment": {
                "type": "container_reference", "container_id": container.id,
            }}, {"type": "web_search"}],
            tool_choice="required",
            input=("Read and use the mounted cmmc-advisor SKILL.md and its routed "
                   "references to answer this question. Search current primary "
                   "sources before asserting product or authorization status. "
                   "If current evidence is unavailable, say so.\n\n"
                   f"{scenario['prompt']}"),
        )
        return response.output_text, _skill_read_observed(response)
    finally:
        client.containers.delete(container.id)


def run_scenario(client, path: Path, rubric: str, model: str,
                 evaluator_model: str, bundle: bytes) -> dict:
    scenario = load_scenario(path)
    answer, skill_read = invoke_subject(client, scenario, model, bundle)
    if not skill_read:
        raise RuntimeError(f"{scenario['id']}: no read of mounted SKILL.md observed")
    precheck = run_precheck(answer, scenario)
    score = score_response(client, scenario, answer, rubric, precheck, evaluator_model)
    return {
        "scenario_id": scenario["id"], "scenario_path": str(path),
        "subject_model": model, "evaluator_model": evaluator_model,
        "skill_read_observed": skill_read,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "response": answer, "precheck": precheck, "score": asdict(score),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scenario", type=Path, help="scenario YAML file or directory")
    parser.add_argument("--rubric", type=Path, default=DEFAULT_RUBRIC)
    parser.add_argument("--out-dir", type=Path, default=RESULTS_DIR)
    parser.add_argument("--model", default="gpt-6-astra")
    parser.add_argument("--evaluator-model", default="gpt-6-astra")
    parser.add_argument("--dry-run", action="store_true",
                        help="validate package and scenarios without API calls")
    args = parser.parse_args()

    paths = sorted(args.scenario.glob("*.yaml")) if args.scenario.is_dir() else [args.scenario]
    if not paths or any(not p.is_file() for p in paths):
        parser.error("No scenario YAML files found")
    if not args.rubric.is_file():
        parser.error(f"Rubric not found: {args.rubric}")
    scenarios = [load_scenario(path) for path in paths]
    bundle = skill_zip()
    print(f"Validated {len(scenarios)} scenario(s) and {len(bundle)} skill ZIP bytes")
    if args.dry_run:
        return 0
    if not os.getenv("OPENAI_API_KEY"):
        parser.error("OPENAI_API_KEY is required for live skill evaluations")
    try:
        from openai import OpenAI
    except ImportError:
        parser.error("Install dependencies: pip install -r evals/runner/requirements.txt")

    client = OpenAI()
    rubric = args.rubric.read_text(encoding="utf-8")
    args.out_dir.mkdir(parents=True, exist_ok=True)
    passed = True
    for path in paths:
        result = run_scenario(client, path, rubric, args.model, args.evaluator_model, bundle)
        output = args.out_dir / f"{datetime.now(timezone.utc):%Y-%m-%d-%H%M%S}-{result['scenario_id']}.json"
        output.write_text(json.dumps(result, indent=2), encoding="utf-8")
        print(f"{result['scenario_id']}: passed={result['score']['passed']} -> {output}")
        passed &= result["score"]["passed"]
    return 0 if passed else 2


if __name__ == "__main__":
    sys.exit(main())
