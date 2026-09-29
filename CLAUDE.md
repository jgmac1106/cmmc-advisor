# Project Instructions for AI Agents

This repository distributes the `cmmc-advisor` OpenAI plugin skill. It ships `skills/cmmc-advisor/SKILL.md` plus its `references/` knowledge base, and evaluates the packaged skill through the OpenAI Responses API under `evals/`.

## Scope

Do not treat this repo as a general code project. It is a content-first artifact:

- `skills/cmmc-advisor/SKILL.md` defines the advisor persona and routing table.
- `skills/cmmc-advisor/references/` holds the source material, organized by CMMC domain, level, assessment process, SSP/POA&M guidance, Rev 3 transition notes, and modern IT mapping.
- `evals/` tests the skill's answers against real CMMC scenarios.
- `skills/cmmc-advisor/references/SOURCES.md` lists the public sources behind factual claims. Any new factual assertion must cite a source there before it lands.

## Philosophy

From `README.md`: this skill is an enabler, not a gatekeeper. When a compliant path exists, map it clearly. When no compliant option exists today, identify the gap honestly, describe who is working on closing it, estimate when options may become available, and suggest interim measures.

Every change must preserve that posture. Answers that block, hedge, or refuse without offering a path forward are failures regardless of factual accuracy.

## Evals

The runner at `evals/runner/` mounts the distributed skill folder as an inline ZIP in a fresh OpenAI hosted container for each scenario. It requires an observed shell read of `SKILL.md`, runs a deterministic precheck, and scores with a second Responses call. It tests the skill runtime; a final ChatGPT plugin-host test still requires installing the plugin in ChatGPT.

Usage (run from repo root):
```bash
pip install -r evals/runner/requirements.txt
python -m unittest evals.runner.test_runner
python -m evals.runner.runner evals/scenarios --dry-run
export OPENAI_API_KEY=...
python -m evals.runner.runner evals/scenarios/level-2-scoping-basic.yaml
```

Add scenarios under `evals/scenarios/` as YAML. Add rubrics under `evals/rubrics/` as Markdown. The format is intentionally small so contributors can extend coverage without harness work.

## Source discipline

Every factual claim in the skill (control text, assessment procedures, CMMC level definitions, acronyms, deadlines) must trace to a source in `skills/cmmc-advisor/references/SOURCES.md`. Interpretive guidance (when to choose which cloud, how to draft an SSP narrative) does not require citation but must not contradict cited sources.

When an AI agent edits any file under `skills/cmmc-advisor/`, it must:
1. Verify the factual claim is already in the source register or add the source there.
2. Prefer linking to the authoritative URL over paraphrasing memory.
3. Flag any claim it cannot source rather than guessing.

## Voice

Same voice discipline as the wider Igris-family content: no em dashes, no slop words (delve, utilize, tapestry, paradigm, leverage as verb, etc.), no hedging filler ("It's worth noting", "Importantly"), no teacher voice ("Let me explain"). The skill speaks practitioner-to-practitioner to compliance officers, security engineers, and contracting officers.

## When to use which agent

- Content work on `skills/cmmc-advisor/`: edit directly; test the packaged skill on representative scenarios.
- New domain practice files: author one domain at a time, add at least one eval scenario per new domain.
- Eval runner changes: small repo, direct edits are fine; tests are the scenario runs themselves.

## What this repo does NOT carry

- No hooks or MCP server. This is a skills-only plugin; the API eval runner is separate from the distributed skill.
