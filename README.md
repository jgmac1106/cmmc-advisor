# CMMC Advisor

A ChatGPT and Codex skill for working through CMMC 2.0 (Cybersecurity Maturity Model Certification) compliance. Built for defense contractors who deliver services to the U.S. Government and need clear, actionable guidance on cybersecurity certification requirements.

## Philosophy

This skill exists to help businesses succeed in delivering great services to the U.S. Government in a compliant way. It is not a tool to say no. It is a tool to say **how**.

When a compliant path exists, the skill maps it clearly. When no compliant option exists today, the skill identifies the gap, describes who in the industry is working on closing it, and estimates when options may become available. Legitimate gaps in the market deserve honest answers, not dead ends.

## What This Covers

All three CMMC levels: Level 1 (Foundational), Level 2 (Advanced), Level 3 (Expert). 14 domains, 110 practices with full implementation guidance mapped from NIST SP 800-171 Rev 2. Assessment preparation for self-assessment, C3PAO, and DIBCAC paths. CUI scoping covering boundary definition, FCI vs CUI, and enclave strategies. SSP guidance, objective-level traceability matrices, evidence inventories, change-impact reviews, and POA&M management.

Modern IT compliance mapping for real-world stacks:

- Cloud platforms. AWS GovCloud, Azure Government, GCP Assured Workloads, and hybrid patterns.
- Productivity suites. Microsoft 365 GCC and GCC High, Google Workspace, Atlassian Government Cloud, ServiceNow GCC, GitHub Enterprise, Box for Government.
- AI services. FedRAMP-authorized (Amazon Bedrock GovCloud, Azure OpenAI Government, Vertex AI Assured Workloads), self-hosted (Coder, on-prem LLM, air-gapped), and AI dev tools (Claude Code, Copilot Enterprise, Cursor, Windsurf, Continue).
- Endpoint management. macOS, Windows STIG baselines, remote work.

Contractor-specific guidance by company size (small, medium, large) and socioeconomic set-aside (SDVOSB, 8(a), WOSB/EDWOSB, HUBZone).

FedRAMP Marketplace practitioner guide with curated category short-lists, search guidance, and coverage-gap analysis.

Rev 3 transition context (current Rev 2 requirements with Rev 3 awareness).

Anti-patterns catalog: sixteen named compliance-theater patterns across documentation, tool, scope, and assessment categories.

## OSCAL JSON Interoperability

The traceability workflow includes OSCAL JSON guidance for NIST SP 800-171 Revision 2. It maps canonical SSP implementations, assessment plans, evidence observations/results, and POA&M content into native OSCAL models while keeping a reviewed objective-level crosswalk. The current NIST `oscal-content` tree provides an SP 800-171 Rev. 3 catalog; a separately verified Rev. 2 catalog must be pinned and reviewed, not silently replaced with Rev. 3. A candidate is [Archstone Security's Rev. 2 combined catalog and profile](https://github.com/khanssen/oscal-nist-800-171r2) (OSCAL 1.1.2; CC BY 4.0; third-party, not NIST published). Its token-safe control IDs (such as `_03.08.01`) require mapping from human-facing IDs (`3.8.1`). Verify releases, provenance, and source-text fidelity before use. JSON must pass a pinned OSCAL schema before any schema-valid claim. Do not publish client CUI or evidence to this public repository. See [OSCAL Rev. 2 interoperability](skills/cmmc-advisor/references/oscal-rev2-interoperability.md).

## Installation

This repository is a skills-only OpenAI plugin. The portable manifest is `plugin.json`; the complete skill, including its references and license, is under `skills/cmmc-advisor/`. There is no MCP server or credential requirement.

For ChatGPT on the web, install the plugin after it has been packaged and made available through the ChatGPT Plugins Directory. A repository clone by itself does not install a skill into ChatGPT on the web. Plugin authors can use the [OpenAI plugin packaging guide](https://developers.openai.com/plugins/build/plugins) and [submission guide](https://developers.openai.com/plugins/deploy/submission) to test and distribute it.

For local Codex use, clone this repository and copy the skill folder to your personal skills directory:

```bash
git clone https://github.com/LV-262/cmmc-advisor.git
mkdir -p ~/.agents/skills
cp -R cmmc-advisor/skills/cmmc-advisor ~/.agents/skills/cmmc-advisor
```

For a project-scoped Codex skill, copy that same folder to `<project>/.agents/skills/cmmc-advisor`. The `references/` directory and its `SOURCES.md` must remain next to `SKILL.md`.

## Usage Examples

```
"What CMMC level do I need for a DoD subcontract that handles CUI?"

"We use Google Workspace and macOS. Can we achieve Level 2 compliance?"

"Design a CUI enclave for a 30-person company using AWS GovCloud."

"What evidence do I need to collect for the Access Control domain?"

"Build an objective-level traceability matrix from our canonical SSP, approved plans, and collected evidence."

"Compare our revised Media Protection Plan with the traceability matrix and flag affected objectives."

"We want to use AI coding tools in our development workflow. What are the compliant options?"
```

## Sources

Every factual claim in this skill traces to a publicly available source. See [SOURCES.md](skills/cmmc-advisor/references/SOURCES.md) for the complete provenance list.

Primary sources include:
- NIST SP 800-171 Revision 2 and SP 800-171A (Assessment Procedures)
- 32 CFR Part 170 (CMMC Program Final Rule) and 48 CFR acquisition rule
- CMMC Assessment Guide Level 2 (dodcio.defense.gov)
- DoD CSP SRG v1r1 (public.cyber.mil) for DoD Impact Level reciprocity
- FedRAMP Marketplace (fedramp.gov) for authorization status
- NIST CMVP Validated Modules Registry (csrc.nist.gov) for FIPS validation
- SBA regulations (13 CFR Parts 121/124/126/127/128) for contractor profiles
- Cloud provider compliance documentation (AWS, Microsoft, Google Cloud)
- Vendor trust centers for each named product

Compliance facts that depend on current authorization state (per-service FedRAMP status, per-model availability, vendor product scope) carry dated verification stamps inline, typically "verified 2026-04-21 via [URL]." Re-verify at the primary source before citing in an SSP.

The [September 2026 targeted claim review](evals/CLAIM_AUDIT.md) identifies contradicted Microsoft tenancy assertions and outdated AI-tool grading assumptions. It does not validate the entire corpus.

## Evaluations

The runner packages the actual `skills/cmmc-advisor/` folder as an inline ZIP,
mounts it in a fresh OpenAI hosted shell container for each scenario, and
requires evidence that the model read `SKILL.md` before scoring its answer.
This exercises the distributed skill in the OpenAI skill runtime. After the
plugin is available in ChatGPT, also test it in a new ChatGPT conversation.
The subject has web search available for current primary-source checks.

```bash
pip install -r evals/runner/requirements.txt
python -m unittest evals.runner.test_runner
python -m evals.runner.runner evals/scenarios --dry-run
OPENAI_API_KEY=your_key python -m evals.runner.runner evals/scenarios
```

`--dry-run` validates scenarios and ZIP layout without API calls. Live runs
require an API key, create one hosted container per scenario, and save graded
JSON results in `evals/results/`. Review the current source evidence yourself
before using any answer in an SSP.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines. Key requirement: every factual claim must cite a public source.

## Disclaimer

This skill provides compliance guidance based on publicly available documentation. It is not legal advice, it is not a substitute for professional cybersecurity consultation, and it does not constitute an official assessment or certification. Always verify guidance against current authoritative sources and consult qualified professionals for your specific situation.

## License

Released under the [MIT License](LICENSE). Copyright (c) 2026 J. Gregory Mcverry as a fork of Copyright (c) 2026 Lloyd Evans.

Free to use, modify, and redistribute, including commercially. If you fork, adapt, or build on this skill, keep the copyright notice and license text intact. Attribution in a visible place (README, about page, skill frontmatter) is appreciated but not legally required beyond what the license specifies.
