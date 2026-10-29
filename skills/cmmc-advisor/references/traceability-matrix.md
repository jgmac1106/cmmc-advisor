# Assessment-Objective Traceability and Evidence Mapping

> Basis: NIST SP 800-171 Rev. 2, NIST SP 800-171A, CMMC Level 2 Assessment Guide, 32 CFR Part 170. This is a practitioner workflow, not an assessor determination.

## Trigger and outputs
Use when asked to build, refresh, audit, or reconcile a CMMC traceability matrix, map evidence, or assess the impact of revised plans. Outputs: (1) objective-level traceability workbook, (2) evidence inventory, (3) missing-evidence/validation queue, and (4) change-impact report. For Level 2, reconcile against the authoritative 110 practices and 320 assessment objectives; never fabricate missing objectives or alter their official wording.

## Intake and source-of-truth hierarchy
1. Confirm organization, assessment level/revision, CUI boundary, authoritative objective catalog, canonical SSP version, approved policies/plans/SOPs, technical evidence, gap analysis, and POA&M.
2. Ask for missing canonical inputs; if unavailable, produce a clearly labeled partial matrix with unverified entries.
3. Use the **canonical SSP** for implementation statements, the official assessment guide for objective wording, approved versioned documentation for documentary mappings, and observed records for operational mappings.
4. The gap analysis supplies prior assessment results; the POA&M supplies remediation references. Neither replaces the SSP or official objectives.
5. Never bring client-specific sources from a different client/project without explicit authorization. Do not put CUI, credentials, controlled screenshots, or customer evidence into public GitHub repositories or unapproved AI services.

## Workbook specification
**Objective Matrix**: practice ID, objective ID, verbatim objective text/source version, SSP statement/version/location, policy ID/version/section, plan/SOP ID/version/section, implementation mechanism, evidence IDs, examine/interview/test method, evidence sufficiency, evidence collection status, accountable owner, last verified, prior assessment determination, proposed change, reviewer decision, POA&M ID, reviewer notes.

**Evidence Inventory**: unique stable evidence ID, artifact title/type, exact file or secure repository locator, source system, owner, version, collection date, period covered, sensitivity/handling restriction, applicable objective IDs, collection method, integrity/hash if available, validation status, next refresh trigger. Reuse one evidence ID across objectives rather than copying the artifact.

**Change Log**: changed source and version, previous mapping, new mapping, impacted objective IDs, contradiction or gap, reviewer, approval date. **Evidence Requests**: objective ID, required evidence, owner, priority, requested date, state, related POA&M ID.

## Four-pass workflow
1. **Document mapping:** parse every official objective and preserve its text. Map exact sections of approved documents and canonical SSP statements. A policy/plan/SOP can establish a definition, designation, or documented procedure when the objective asks for one; record that documentary support without asserting operational effectiveness.
2. **Operational evidence:** map configuration exports, logs, access reviews, tickets, training completions, tests, physical records, and interviews where relevant. Verify scope, dates, system identity, and whether evidence actually proves the asserted mechanism. Distinguish provider-inherited controls from contractor responsibilities.
3. **Validation:** label each objective Supported / Partially supported / Unsupported / Pending validation, with separate documentary and operational sufficiency. Flag stale, contradictory, unapproved, and missing artifacts. These are internal mapping labels, not official CMMC MET/NOT MET determinations.
4. **Reconciliation:** compare against gap analysis and POA&M; create review recommendations and evidence requests. Never silently overwrite SSP statements, assessment status, or POA&M records.

## Incremental change-impact review
On a revised policy/plan/SOP or architecture change: compare versions; identify changed statements and referenced objectives; recheck exact mappings and affected implementation evidence; mark stale links; produce a before/after change log and proposed SSP/gap-analysis edits for approval. Preserve unaffected rows and evidence IDs. Revalidate any changed boundary, CUI flow, technical control, or inherited responsibility.

## Quality gates
- All official objectives accounted for exactly once in the Objective Matrix; no invented IDs or objective text.
- Every cited artifact has a resolvable locator, version, exact section, and source owner; missing data explicitly flagged.
- Every assertion has a source; no fabricated screenshots, logs, configuration, or interview results.
- Documentation sufficiency never automatically implies implementation or a MET assessment.
- Source conflicts and gaps are visible; no automatic reassessment.
- Verify workbook row counts, unique objective IDs, cross-sheet evidence references, filters, and preserved formulas before delivery.
- Treat refresh schedules as organization-specific unless mandated; preserve evidence collection timestamps and change triggers.

## Example invocation
"Build the Level 2 objective-level traceability matrix from our canonical SSP and approved plans. Map each objective to exact sections and existing operational evidence, flag missing proof, preserve the gap analysis, and output the workbook plus change report."

See `evidence-collection.md` for evidence categories and `ssp-guidance.md` for authoritative SSP maintenance.


## Machine-readable OSCAL output

Follow `oscal-rev2-interoperability.md` for OSCAL JSON model selection, Rev. 2 catalog provenance, objective crosswalks, strict schema validation, secure evidence links, and SSP/Assessment Plan/Assessment Results/POA&M exports. Do not treat a custom traceability JSON schema as an OSCAL document or substitute NIST 800-171 Rev. 3 content for the Rev. 2 baseline.
