# OSCAL JSON Interoperability for CMMC Level 2 / NIST SP 800-171 Rev. 2

## Scope and source discipline
Produce OSCAL-compatible JSON using the published OSCAL **model schemas**, while keeping the *security control baseline* explicitly at NIST SP 800-171 **Revision 2** and CMMC Level 2 assessment objectives. The model schema version and control baseline revision are independent. Do not confuse OSCAL v1.x with SP 800-171 Rev. 2.

NIST OSCAL source repositories:
- Content: https://github.com/usnistgov/oscal-content
- Schemas and model definitions: https://github.com/usnistgov/OSCAL
- Models: https://pages.nist.gov/OSCAL/learn/concepts/layer/
- Assessment models: https://pages.nist.gov/OSCAL/learn/concepts/layer/assessment/

**Availability caveat:** As reviewed 2026-10-29, the current `oscal-content/nist.gov/SP800-171/` tree exposes `rev3`, not `rev2`. Do **not** import a Rev. 3 catalog or relabel it as Rev. 2. Obtain a separately reviewed faithful Rev. 2 catalog from an authoritative Rev. 2 source, or build a local Rev. 2 catalog with recorded provenance and review; never claim it was published by NIST unless verified. Track a pinned URI/commit, SHA-256 digest and publication/revision metadata for the chosen catalog, plus a separately sourced Rev. 2 assessment-objective mapping. Do not invent official assessment objective identifiers or assume the OSCAL catalog automatically includes every 800-171A objective.

## Reviewed third-party Rev. 2 OSCAL candidate (2026-10-29)
The public [khanssen/oscal-nist-800-171r2](https://github.com/khanssen/oscal-nist-800-171r2) repository (Archstone Security LLC, K. Stanford, release version `2.0-combined.1`) provides:
- Catalog: `catalog/nist-sp-800-171r2-combined-catalog.json` (OSCAL 1.1.2). Its documentation states 14 groups, 110 Rev. 2 requirements, 320 SP 800-171A objective parts, and 110 assessment procedures. These are **publisher claims** until independently checked against the official NIST source, pinned release and schema.
- Profile: `nist-sp-800-171r2-profile.json`, importing all 110 controls from that catalog. For an SSP importing the profile, use this pinned local/profile reference; do not substitute a Rev. 3 profile.
- Provenance and verification: `README.md`, `DIFFERENCES.md`, `CORRECTIONS.md`, `scripts/validate.py`, GitHub release attestation and release `SHA256SUMS`. Verify the specific release asset and attestation with `gh attestation verify <file> --owner khanssen`, compare its SHA-256, run the published validator, and spot-check requirement/objective text against NIST Rev. 2 and 800-171A. A successful attestation proves artifact provenance, **not** content correctness.
- Licensing: the combined curation/OSCAL structure is offered under **CC BY 4.0**, with attribution to "NIST SP 800-171 Rev 2 Combined OSCAL Catalog, Archstone Security LLC, https://github.com/khanssen/oscal-nist-800-171r2". Respect license and attribution if redistributing or adapting. Do not imply NIST endorsed the third-party rendering.

**Review caveat:** At inspection, the upstream README contains unresolved Git merge conflict markers in its objective documentation (`a` through `o` versus `a` through `n`). Do not rely on that README sentence to enumerate objective parts. Read the catalog itself and run the 320-objective count/letter-sequence checks. These files are **a candidate source**, not automatically verified or bundled as an authoritative baseline.

### Exact ID crosswalk required for this catalog
The catalog uses OSCAL token-safe control `id` values such as `_03.08.01` and objective part IDs such as `_03.08.01_obj.a`; its `label` property is the familiar `3.8.1` and the human assessment objective is `3.8.1[a]`. Record all of:
- `control_id = "3.8.1"` (human NIST number);
- `oscal_control_id = "_03.08.01"` (actual OSCAL `control.id` and imported SSP `control-id`);
- `objective_id = "3.8.1[a]"` (human objective);
- `oscal_objective_part_id = "_03.08.01_obj.a"` (actual catalog `part.id`).

Do not import `3.8.1` into an OSCAL SSP's `implemented-requirements[].control-id` when using this third-party catalog: the resolvable value is `_03.08.01`. Resolve IDs from the catalog's `label` props and `parts`; never generate IDs by padding without checking against the pinned actual catalog. The source `assessment` parts hold EXAMINE/INTERVIEW/TEST procedures, while objective parts hold the individual determinations.

## OSCAL document crosswalk
| Use case | OSCAL model / native assemblies |
| --- | --- |
| Normative 800-171 Rev. 2 control language | Catalog (`catalog`, `groups`, `controls`) or Profile importing a reviewed Rev. 2 Catalog |
| Reusable technology implementation | Component Definition (`component-definition`) when applicable |
| Organization-specific SSP | System Security Plan (`system-security-plan`, `import-profile`, `system-implementation`, `control-implementation`, `implemented-requirements`) |
| Proposed assessment scope and examine/interview/test tasks | Assessment Plan (`assessment-plan`, `import-ssp`, `reviewed-controls`, `tasks`) |
| Collected observations, evidence, findings | Assessment Results (`assessment-results`, `import-ap`, `results`, `observations`, `findings`, `risks`) |
| Corrective actions and risk remediation | POA&M (`plan-of-action-and-milestones`) |
| Evidence file references | OSCAL `back-matter.resources`, `rlinks` or permitted attachments, referenced by UUID |
| Extra traceability metadata | OSCAL `props` and `links` where the *selected model location* permits them; use named namespace + stable values |

## Objective-level mapping
Use original 800-171 Rev. 2 IDs such as `3.8.1` as the control key and keep CMMC notation (e.g. `MP.L2-3.8.1`) as a cross-reference, not a replacement control ID. Preserve assessment objective IDs like `3.8.1[a]` using reviewed 800-171A/CMMC Assessment Guide source text and documented mappings to the parent control. An objective may map to a catalog `part` or assessment plan `objective` **only if** the target object's allowed schema actually supports that representation; otherwise store a namespaced extension `prop`/link in a permitted OSCAL assembly and a validated sidecar crosswalk. Do not claim the crosswalk sidecar is itself an OSCAL model.

Keep a separate objective mapping when source catalogs lack the objective text; record each objective's citation, source version, parent control ID, method (EXAMINE / INTERVIEW / TEST), SSP statement locator, evidence UUIDs, documentary sufficiency and operational sufficiency, human reviewer, and review date. Never encode internal mapping labels as assessor findings. Create official OSCAL findings only when an actual assessment has been conducted and a reviewer has authorized the determination.

## Validation and publication gates
1. Pin a specific OSCAL JSON schema release from `usnistgov/OSCAL`; save schema URL/version and digest. Do not infer the schema version from a Rev. 2 baseline.
2. Generate documents with the standard OSCAL root keys, mandatory UUIDs, `metadata`, required imports and correct references for the selected model. Do not guess a structural key: inspect schema first.
3. Validate JSON with a JSON parser and **the actual pinned OSCAL JSON schema**, then perform cross-document import/UUID/reference checks, Rev. 2 control-ID checks, objective completeness/uniqueness checks and allowed-property-placement checks.
4. Use native OSCAL imports and UUID-based resource references rather than embedding duplicate controls or CUI evidence. Keep evidence in an approved protected repository; public GitHub may store schemas, non-sensitive templates and redacted examples only.
5. On a substantive file edit rotate the **document root UUID** and update `metadata.last-modified`; preserve stable UUIDs of unchanged underlying resources where appropriate. Do not claim schema-valid output until a validator has actually passed.
6. Generate the Excel traceability matrix as a **view/export** over the reviewed objective crosswalk plus OSCAL documents, not a competing source of truth. Keep the canonical organization SSP as authoritative until an approved OSCAL migration is completed.
7. Separate three labels: `OSCAL-schema-valid` (syntax/structure tested), `Rev2-content-reviewed` (source fidelity verified), and `assessment-verified` (human evidence/implementation assessment). One does not imply another.

## Example metadata rule
For a control linked in an SSP, set `implemented-requirements[].control-id` to the **actual imported catalog control ID**. With the Archstone catalog above, use `"_03.08.01"` for requirement 3.8.1, not `"3.8.1"`. Associate `3.8.1[a]` through a reviewed objective crosswalk and appropriately named property/link or assessment planning structure; do not invent `objective-id` fields unsupported by OSCAL schema.

## Machine-readable companion schema

The repository includes `schemas/rev2-objective-crosswalk.schema.json` (JSON Schema Draft 2020-12) for validating the **companion objective crosswalk only**. Its `objective_id` maps to `control_id`; evidence may refer to native OSCAL `back-matter.resources` UUIDs. A valid crosswalk is **not** proof that an accompanying OSCAL document passes its official OSCAL schema; run both validations. Use a locally pinned, independently reviewed catalog URI and source provenance; the third-party catalog is a documented candidate, not bundled or implicitly NIST-approved.

## Client isolation
Never upload actual customer SSPs, CUI content, assessment evidence, architecture details or personal information to this public repository. Only generalized schemas, workflows, templates and clearly synthetic examples belong here.
