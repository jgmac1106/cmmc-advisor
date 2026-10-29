# Microsoft 365 GCC and GCC High Compliance

> **Authorization review: 2026-10-29.** Microsoft descriptions, government
> Marketplace records, and DoD impact-level equivalency are separate evidence.
> Read "FedRAMP and Impact Level posture" below for the dated reconciliation
> and source links. Other feature guidance remains subject to current checks.

## Overview

This file maps Microsoft 365 tenancy patterns to CMMC practice
requirements for defense contractors handling CUI or FCI. It is
the authoritative source in this corpus for the GCC versus GCC
High versus DoD tenancy-selection decision. Phase 5b's
`references/modern-it/endpoints/windows-fleet.md` carries a
compact pointer to this file for the full decision tree per hub
Decision 5.

Microsoft 365 government tenancies serve distinct audiences:

- **Commercial.** Keep non-CUI work here where the contract permits. Do not
  use the GCC package as evidence for Commercial productivity services.
- **GCC.** Evaluate against the actual CUI category, contract, and service
  boundary; see the unresolved vendor/Marketplace classification difference below.
- **GCC High.** Evaluate for workloads needing its government boundary and
  export-control commitments. Its name does not establish a DoD PA.
- **DoD.** Microsoft limits purchase to DoD entities. Contractors must verify
  eligibility and the mission owner's authorization path rather than assume access.

Read this file alongside
`references/modern-it/productivity/README.md` (the Phase 5d hub
carrying the seven conventions including the canonical
capability-appendix format), the Phase 5c cloud-platforms hub
(`references/modern-it/cloud-platforms/cloud-selection.md`) for
the FedRAMP-to-IL crosswalk under CSP SRG v1r1, and
`references/modern-it/cloud-platforms/azure-government.md` for
the Azure IaaS and platform services that M365 GCC High runs
on top of.

**Current tier summary.** Use the source-separated table in "FedRAMP and
Impact Level posture" and `references/data/fedramp-snapshot.json`. An offering's
listing does not establish authorization for every feature or customer workflow.

---

## Scope of this file

Covered:

- Microsoft 365 commercial, GCC, GCC High, and DoD tenancy
  posture for defense contractors handling CUI or FCI.
- Tenancy and subscription model; identity plane (Entra ID
  Government, Conditional Access, PIM); productivity core
  (Exchange Online, SharePoint Online, OneDrive for Business,
  Teams); endpoint management plane (Intune); compliance and
  governance (Microsoft Purview); security operations (Defender
  for Office 365, Defender for Endpoint); Power Platform.
- CMMC practice mapping per capability cluster.
- Evidence-collection patterns.
- Common mistakes specific to M365 government tenancies.
- ITAR story for GCC High, distinct from Google Workspace
  Assured Controls Plus (see `google-workspace.md`).

Not covered:

- Azure IaaS and platform services. Those live in
  `references/modern-it/cloud-platforms/azure-government.md`.
  M365 GCC High and Azure Government are separate tenancies
  that interoperate; the Azure file handles platform posture,
  this file handles productivity posture.
- Endpoint configuration detail for Windows fleets under Intune.
  Capability-to-practice mapping for Windows endpoints lives in
  `references/modern-it/endpoints/windows-fleet.md`.
- Microsoft 365 DoD tenancy in implementation depth. The DoD
  tenancy is for DoD mission owners; contractors interact with
  DoD tenants through cross-tenant collaboration rather than
  landing there directly.
- Microsoft 365 Copilot and generative-AI features. Productivity
  AI features carry separate FedRAMP scope considerations
  covered under `references/modern-it/ai-services/`.
- Pre-2016 legacy offerings (Office 365 E3 Government, older
  GCC naming). The current GCC / GCC High / DoD taxonomy is
  the authoritative one.

---

## Tenancy Selection

Record the following before recommending a migration or claiming inheritance.

**1. Establish the contract and data flow.** Identify FCI, CUI/CDI categories,
export-controlled data, and every place the workload stores, processes, or
transmits them. Read the actual clauses and flow-downs, CMMC assessment
requirement, agency conditions, and any explicit DoD IL requirement. Distinguish
contractor systems from an IT service operated on behalf of the Government.
[DFARS 252.204-7012](https://www.acquisition.gov/dfars/252.204-7012-safeguarding-covered-defense-information-and-cyber-incident-reporting.)
(b)(1) and (b)(2) use different paths. Paragraph (b)(2)(ii)(D) requires an
external CSP handling CDI to meet the FedRAMP Moderate-equivalent baseline
and paragraphs (c)-(g); it does not itself prescribe GCC High, FedRAMP High,
a DoD IL5 PA, or a particular CMMC assessment type. Verified 2026-10-29.

**2. Evaluate the tenancy for that workload.**

- **Commercial:** Microsoft's current [compliance explanation][ms-comparison]
  excludes Commercial productivity data enclaves from the GCC FedRAMP package.
  Conditional Access and DLP cannot expand that boundary. Keep Commercial for
  non-CUI workflows where permitted; isolate CUI in an appropriately supported
  environment or migrate the affected workflows. Verify separately authorized
  Azure services separately, even when bundled in the same Microsoft license.
- **GCC:** Consider it when the CUI category and written contract requirements
  fit. Microsoft describes DFARS 7012 flow-down support, with CUI limitations.
  Obtain the applicable agreement, attestation, and package scope, including
  incident obligations (c)-(g). Resolve any required High-level coverage against
  the differing source descriptions below before relying on it.
- **GCC High:** Consider it for the government boundary and export-control
  requirements. Verify applicable contractual commitments and service scope.
  IL4 equivalency is a vendor description, not evidence of a DISA IL4/IL5 PA.
- **An explicit IL5 requirement:** Request the current service-specific DoD
  authorization, conditions, and mission-owner acceptance. Do not route this
  automatically to GCC High. Microsoft's DoD offering has different eligibility;
  evaluate an eligible authorized service with the contracting/mission owner.

**3. Verify each service and dependency.** Inventory mail, files, Teams,
identity, Intune, Defender, Purview, Power Platform, AI features, connectors,
backup, telemetry, support, and cross-tenant access. Record the SKU, cloud,
feature, region where applicable, data path, package ID, current status,
authorization boundary, source URL, and access date. Check exclusions and
customer responsibilities in the package/ATO and service documentation.
A Microsoft 365 license can bundle services covered by different Microsoft 365
and Azure packages. Neither availability nor bundling proves authorization.
[Microsoft's scope matrix][ms-scope] is a starting index; obtain the applicable
package evidence before claiming inherited controls.

**4. Verify personnel and support boundaries.** Microsoft's [GCC High/DoD
service description][ms-gcch] documents citizenship screening for personnel
accessing customer content. It separately excludes customer support from the
service accreditation boundary. Keep CUI out of ordinary support tickets and
confirm an approved support channel and recipient authorization before sharing.
Evaluate contractor and guest access under the actual export-control terms;
a tenant purchase does not authorize an export or make all personnel eligible.

**5. Document the decision.** Keep a contract-to-service matrix and shared-
responsibility record in the SSP evidence set. If a status, scope, or contract
condition cannot be established, mark it **unverified** and identify the
specific evidence needed. Offer a scoped enclave, an eligible alternative,
or a staged migration while the missing evidence is obtained. Do not replace
uncertainty with either blanket approval or blanket exclusion of GCC.

---

## Tenancy and subscription model

**Capability.** A Microsoft 365 tenancy is the top-level unit
of isolation; each tenancy has a unique domain
(`contoso.onmicrosoft.us` for GCC High) and distinct identity,
licensing, and service-scope boundaries. Within a tenancy,
Microsoft 365 licenses provision service entitlements per user
(Office 365 E5 GCC High, Microsoft 365 E5 GCC High, and
similar bundles). The same corporate entity may operate
multiple M365 tenancies (for example, a commercial tenancy for
non-CUI work plus a GCC High tenancy for CUI work); cross-tenancy
collaboration uses guest-account federation patterns.

**CMMC practices implemented.** CM.L2-3.4.1 (baseline
configuration), CM.L2-3.4.2 (configuration enforcement),
AC.L2-3.1.3 (CUI flow control at tenancy boundaries), and
AC.L2-3.1.5 (least privilege at the tenancy administrative
role level).

**Implementation notes.**

- Operate separate commercial and GCC High tenancies when the
  organization has both non-CUI work and CUI work. Merging the
  two into one tenancy is not technically possible at the
  service-plane level; the tenancies are architecturally
  distinct.
- License administration happens through the Microsoft 365
  admin portal for the tenancy. GCC High licensing is priced
  separately from commercial and is sold through specific
  authorized reseller channels; verify reseller status before
  purchasing.
- Use tenant-level settings (Global Administrator scope) as a
  last-resort emergency pattern; delegate day-to-day
  administration through specific roles (User Administrator,
  Compliance Administrator, SharePoint Administrator, Teams
  Administrator, Security Administrator, Exchange
  Administrator) with PIM just-in-time activation.
- Cross-tenant collaboration between GCC High and commercial
  or between GCC High and other GCC High tenants uses the B2B
  guest-account pattern plus Entra External ID Government
  configuration. The cross-tenant identity federation must be
  documented in the SSP.

**Evidence to collect.**

- Tenancy registration documentation showing the tenancy's
  GCC High designation.
- License inventory showing service entitlements per user.
- Admin role assignments documentation (via PIM or equivalent).
- Cross-tenant federation configuration if applicable.

**Common mistakes.**

- Provisioning a single commercial tenancy with the intent to
  "add a GCC High overlay later." The overlay does not exist;
  GCC High is a separate tenancy.
- Using Global Administrator for day-to-day operations. Role
  sprawl and blast-radius concerns make this a common
  assessment finding.
- Cross-tenancy federation without Conditional Access policies
  on the guest-account plane. External users accessing CUI
  require the same MFA and posture enforcement as internal
  users.

---

## Identity and access management

**Capability.** Microsoft Entra ID Government is the identity
service for GCC High tenancies (formerly Azure AD Government).
Entra ID Government supports Conditional Access policies
(session-level risk-based enforcement), Privileged Identity
Management (just-in-time role activation with approval
workflows), multi-factor authentication enforcement, external
identity federation (SAML, OIDC, SCIM), and hybrid identity
through Entra Connect from on-premises Active Directory.

**CMMC practices implemented.** IA.L1-3.5.1 (user
identification), IA.L1-3.5.2 (user authentication),
IA.L2-3.5.3 (MFA), IA.L2-3.5.4 (replay-resistant
authentication), AC.L2-3.1.1 (account management),
AC.L2-3.1.5 (least privilege), AC.L2-3.1.7 (privileged
function logging through PIM activation events), and
AC.L2-3.1.8 (unsuccessful logon attempts through Conditional
Access lockout).

**Implementation notes.**

- Match the identity design to the chosen service cloud and supported
  federation. GCC pairs with Entra ID in Azure; GCC High and DoD pair with
  Entra ID in Azure Government ([Microsoft integration][ms-integration],
  verified 2026-10-29). Scope identity dependencies and verify their own
  authorization and contract fit; CUI alone does not prescribe one identity cloud.
- Conditional Access policies should require phishing-
  resistant MFA (FIDO2 security keys, Windows Hello for
  Business, or certificate-based authentication) for
  privileged actions and for all CUI-scope applications.
  SMS-based MFA is deprecated by NIST SP 800-63B for
  Authenticator Assurance Level 2 and should not be the sole
  factor for CUI access.
- PIM for Entra ID roles, Azure roles, and PIM for Groups
  delivers just-in-time privileged access. Standing privileged
  assignments should be the exception, not the default.
- Hybrid identity patterns: Entra Connect synchronizes from
  on-premises Active Directory to Entra ID Government. For
  contractors with existing on-prem AD handling CUI identity,
  Entra Connect is the typical integration path; the on-prem
  AD becomes an in-scope identity source. This pulls on-prem
  AD infrastructure (domain controllers, directory databases,
  replication traffic) into CMMC scope for AC, AU, IA, and
  SC practice evidence; the on-prem AD must be documented as
  a CUI-adjacent asset in the SSP and hardened accordingly
  (domain controller patching under SI.L1-3.14.1, AD audit
  logging under AU.L2-3.3.1, privileged group monitoring).
- Entra External ID Government handles B2B guest access to
  CUI resources. Guest users require the same MFA and
  Conditional Access posture as members.

**Evidence to collect.**

- Entra ID Government tenant configuration showing the
  directory location (Government cloud) and identity provider
  configuration.
- Conditional Access policy export with MFA and session-
  control policies applied to CUI scope.
- PIM role assignment inventory (just-in-time vs permanent).
- Authentication methods policy showing phishing-resistant
  methods enforced.
- Sign-in log sample from Entra ID forwarded to the SIEM.

**Common mistakes.**

- Ignoring an external identity provider in the boundary analysis. Verify
  supported federation, authentication data flows, and the provider's role
  and obligations before claiming control inheritance.
- Using SMS or phone-call MFA as the primary factor. Phishing-
  resistant methods are the assessor-preferred default.
- Granting standing Global Administrator to staff. PIM-
  eligible-only is the default; standing assignment is a
  deliberate exception with documented justification.

---

## Productivity core: Exchange Online, SharePoint Online, OneDrive, Teams

**Capability.** The productivity core of M365 GCC High
comprises Exchange Online (email, calendar, distribution
lists); SharePoint Online (site collections, document
libraries, intranet); OneDrive for Business (per-user file
storage and synchronization); and Microsoft Teams (persistent
chat, channels, meetings, calls, file sharing integrated with
SharePoint and OneDrive). Each service ships in the GCC High
tenancy with distinct authorization scope documented at the
GCC High package (FR1824057433), subject to current scope verification.

**CMMC practices implemented.** AC.L2-3.1.3 (CUI flow control
between services), AC.L2-3.1.18 (mobile device connection
control for Outlook mobile, Teams mobile, SharePoint mobile),
SC.L2-3.13.8 (transmission confidentiality and integrity),
SC.L2-3.13.11 (FIPS-validated cryptography at rest),
SC.L2-3.13.16 (data at rest encryption), AU.L2-3.3.1 (audit
event creation), AU.L2-3.3.2 (user accountability).

**Implementation notes.**

- Exchange Online Protection (EOP) and Defender for Office 365
  provide anti-phishing, anti-malware, and attachment scanning
  for email. Defender for Office 365 is the CUI-expected tier
  for CMMC L2 because the threat environment includes phishing
  and supply-chain email attacks.
- SharePoint Online and OneDrive inherit tenant-level sharing
  policies. Configure the external sharing policy to "New and
  existing guests" or tighter; "Anyone" (anonymous link
  sharing) is not appropriate for CUI-scope site collections.
  Sensitivity labels (Purview) enforce encryption and
  access-control at the document level for CUI.
- Teams channels are backed by SharePoint (team sites) and
  OneDrive (private chat files). CUI shared in Teams chat
  inherits the SharePoint/OneDrive boundary. Private-channel
  and shared-channel patterns have different isolation
  properties; verify channel type before designating CUI
  containers.
- Per-service authorization status for each of these services
  in GCC High must be checked against package FR1824057433 and its scope.
  Not every feature enhancement ships with FedRAMP
  authorization at GA; verify the specific feature
  authorization before relying on it for CUI.

**Evidence to collect.**

- Exchange Online transport rule inventory showing CUI-relevant
  policies (external-sender warning, DLP policies, retention).
- SharePoint external sharing policy configuration export.
- OneDrive tenant sharing policy configuration export.
- Teams governance policy export (guest access, external
  access, messaging policies).
- Defender for Office 365 policy inventory (Safe Attachments,
  Safe Links, anti-phishing, anti-spam).

**Common mistakes.**

- Allowing Anyone (anonymous) sharing links on SharePoint or
  OneDrive in a CUI-scope tenant. Default tenant setting must
  be restricted for CUI.
- Treating Teams persistent chat as ephemeral. Chat messages
  are retained per the tenant's retention policy; CUI shared
  in chat is subject to retention, DLP, and eDiscovery.
- Running Commercial Exchange Online for email while running
  GCC High for files. Email is a common CUI egress path; the
  whole productivity core should live in one tenancy.

---

## Endpoint management plane: Intune

**Capability.** Intune provides endpoint management. Verify the supported
cloud pairing, feature availability, and Intune authorization boundary for the
chosen Microsoft 365 deployment; do not infer these from an E3/E5 license.

**CMMC practices implemented.** CM.L2-3.4.1 (baseline
configuration), CM.L2-3.4.2 (configuration enforcement),
CM.L2-3.4.6 (least functionality), and AC.L2-3.1.18 (mobile
device connection control). See also
`references/modern-it/endpoints/windows-fleet.md` and
`references/modern-it/endpoints/macos-fleet.md` for the
endpoint-side capability-to-practice mapping.

**Implementation notes.**

- Confirm Intune's supported tenant integration and data/telemetry paths.
  Evaluate the exact service against the contract, rather than declaring
  every commercial management service ineligible from its name alone.
- Intune Administrator roles are separate from M365 Admin
  Center roles and from Entra ID roles. Apply PIM to Intune
  role assignments.
- Configuration Service Provider (CSP) policy names evolve
  across Windows feature updates; verify against the current
  Microsoft Learn CSP reference before deploying. See
  `references/modern-it/endpoints/windows-fleet.md` for the
  policy-key rot-protection convention.
- Compliance policies feed Conditional Access device-state
  evaluation. A device must be Intune-enrolled and compliant
  before Conditional Access grants access to CUI workloads;
  this is the endpoint-identity integration pattern.
- Find Intune's applicable scope in [Microsoft's scope matrix][ms-scope]
  and the corresponding authorization package. Do not assign it the Office
  365 package automatically. Check third-party MDM/EDR services separately.

**Evidence to collect.**

- Intune tenancy assignment documentation (GCC High).
- Device inventory report from Intune showing every enrolled
  endpoint's compliance state.
- Configuration profile export showing CUI-scope baselines.
- Conditional Access policies that reference Intune
  compliance state.

**Common mistakes.**

- Assuming a productivity subscription authorizes its management plane.
  Verify service scope and supported integration independently.
- Assuming Intune Administrator role grants Entra ID directory
  access. The role scopes are distinct; separate privileges
  apply.

---

## Compliance and governance: Microsoft Purview

**Capability.** Microsoft Purview (formerly Microsoft 365
Compliance) is the unified compliance platform covering
Data Loss Prevention (DLP), Sensitivity Labels, Retention
Policies
and Labels, Records Management, eDiscovery (Standard and
Premium), Compliance Manager, Communication Compliance,
Information Barriers, and Insider Risk Management. Purview
operates within the M365 tenancy; Purview in GCC High carries
the GCC High tenancy's authorization scope.

**CMMC practices implemented.** AC.L2-3.1.3 (CUI flow control
through DLP), MP.L2-3.8.1 (media marking through sensitivity
labels), MP.L2-3.8.2 (media access restriction through label-
based encryption), AU.L2-3.3.1 (audit event creation),
AU.L2-3.3.2 (user accountability), AU.L2-3.3.5 (audit
correlation through eDiscovery), and CA.L2-3.12.3 (continuous
monitoring through Compliance Manager).

**Implementation notes.**

- Sensitivity Labels are the primary CUI-marking mechanism in
  M365. Create labels aligned with the CUI categories in the
  contractor's scope (for example, "CUI", "CUI//SP-PROPIN",
  "CUI//SP-EXPT"). Labels can auto-apply via content
  inspection, enforce encryption through Azure Rights
  Management, and travel with the document across Exchange,
  SharePoint, OneDrive, and Teams.
- DLP policies detect CUI content in transit (outgoing email,
  external sharing, Teams chat) and block or warn. Start with
  Microsoft-provided CUI-adjacent policy templates and tune
  for the contractor's specific CUI categories.
- Retention Policies enforce the contractor's records-retention
  schedule. CUI typically has longer retention than non-CUI;
  configure retention policies scoped to CUI-labeled content.
- eDiscovery Premium is required for legal-hold workflows on
  CUI. Verify the tenancy's eDiscovery license tier includes
  Premium before relying on it for legal-hold response.
- Compliance Manager provides a scored view of Microsoft-vs-
  customer responsibility per regulatory control. Useful as
  an SSP starting point for inherited controls; not a
  substitute for the contractor's own SSP narrative. See
  `references/modern-it/cloud-platforms/azure-government.md`
  "Microsoft Compliance Manager overlay" for the treatment
  also applicable here.

**Evidence to collect.**

- Sensitivity label configuration export showing CUI labels
  and their encryption and access policies.
- DLP policy inventory showing CUI-detection rules.
- Retention policy configuration scoped to CUI content.
- Compliance Manager assessment export for CMMC Level 2 and
  FedRAMP High, dated.
- Sample eDiscovery case record demonstrating the workflow.

**Common mistakes.**

- Configuring sensitivity labels in the portal but not
  publishing them to a label policy. Created-but-unpublished
  labels are invisible to users.
- Relying on DLP policies without sensitivity labels. DLP can
  detect content patterns (SSN, credit-card, explicit CUI
  markings) but cannot detect contractor-specific CUI content
  categories without a labeling signal.
- Treating Compliance Manager's Microsoft-side attestations
  as completed SSP narrative. Customer-side implementation
  detail remains the contractor's authorship.

---

## Security operations: Defender for Office 365 and Defender for Endpoint

**Capability.** Microsoft Defender for Office 365 provides
anti-phishing, anti-malware, Safe Attachments, Safe Links,
and attack simulation for Exchange Online, SharePoint,
OneDrive, and Teams. Microsoft Defender for Endpoint (MDE)
provides endpoint detection and response (EDR), next-
generation antivirus, threat intelligence, and vulnerability
management for Windows, macOS, Linux, iOS, and Android
endpoints. Both ship in GCC High as separate service
instances from commercial Defender; cross-tenancy data is not
supported.

**CMMC practices implemented.** SI.L1-3.14.2 (malicious code
protection), SI.L1-3.14.4 (update malicious code mechanisms),
SI.L1-3.14.5 (periodic and real-time scanning), SI.L2-3.14.3
(security alerts and advisories), SI.L2-3.14.6 (system
monitoring), and SI.L2-3.14.7 (unauthorized use detection).

**Implementation notes.**

- Defender for Office 365 Plan 2 includes Attack Simulation
  and Threat Explorer; Plan 1 is more limited. For CMMC L2
  CUI workflows, Plan 2 is the expected tier.
- Verify Defender for Endpoint's supported cloud integration and telemetry
  destination against its own scope, the data category, and contract requirements.
- Tamper Protection must be enabled. It prevents local
  administrators from disabling Defender components; this is
  an assessor-typical finding when disabled.
- Telemetry export from Defender to a SIEM handles AU.L2-3.3.5
  correlation. Microsoft Sentinel in Azure Government is the
  natural SIEM pairing; third-party SIEMs ingest via Defender
  APIs.
- Defender Antivirus and a third-party EDR cannot both run in
  active mode simultaneously; configure passive mode for
  Defender when a third-party EDR is the primary.

**Evidence to collect.**

- Defender for Office 365 policy configuration (Safe
  Attachments, Safe Links, anti-phishing policies) exported.
- Defender for Endpoint onboarding status showing every
  managed endpoint is reporting with current signatures.
- Tamper Protection enforcement configuration.
- SIEM forwarding configuration and sample alert record.

**Common mistakes.**

- Leaving Tamper Protection off because it "breaks a tool."
  The assessor expects it on for CUI endpoints.
- Running Defender for Office 365 Plan 1 and assuming it
  covers the SI.L2-3.14.6 monitoring scope. Plan 2 is the
  defensible CMMC L2 tier.
- Exporting telemetry across boundaries without checking supported integration,
  data classification, destination authorization, and contractual restrictions.

---

## Power Platform: Power Apps, Power Automate, Power BI

**Capability.** Power Apps, Power Automate, and Power BI have distinct
service and government-cloud scopes. Verify each environment, connector,
feature, and applicable authorization using [Microsoft's scope matrix][ms-scope].
An M365 tenancy label does not confer an authorization on Power Platform.

**CMMC practices implemented.** When Power Platform is used
for CUI workflows: AC.L2-3.1.3 (CUI flow control), CM.L2-3.4.1
(baseline configuration of data loss prevention policies at
the Power Platform environment level), CM.L2-3.4.2
(configuration enforcement through tenant-level Power
Platform policies), and AU.L2-3.3.1 (audit event creation
through Power Platform audit logs).

**Implementation notes.**

- Power Platform Environments are the primary unit of scope.
  Dedicate Production and Development environments to CUI
  workloads with DLP policies restricting connectors to
  CUI-approved services.
- Connectors to non-CUI services (commercial-Azure data
  sources, third-party SaaS without government tenancy)
  must be blocked at the environment level for CUI-scope
  apps.
- Power Platform GCC High runs on Azure Government
  infrastructure (see
  `references/modern-it/cloud-platforms/azure-government.md`)
  but its authorization scope must be checked independently.
- Audit logs ship to the M365 Compliance audit log; forward
  to SIEM alongside Exchange and SharePoint audit data.

**Evidence to collect.**

- Power Platform tenant-level DLP policy export.
- Environment inventory showing CUI-scope environments and
  their connector policies.
- Audit log configuration for Power Platform.

**Common mistakes.**

- Allowing commercial-connector access from a CUI-scope Power
  Platform environment. The connector-boundary enforcement is
  the primary Power Platform DLP mechanism for CUI.
- Relying on connector DLP alone as the governance surface.
  Connector DLP prevents managed connectors from reaching
  non-approved services but does not prevent a user with
  environment-creator privileges from creating a new
  environment, nor does it prevent personal cloud flows
  reaching personal-account OneDrive or similar. Additional
  governance guardrails needed: restrict environment creation
  to delegated admins, disable personal cloud flows where
  CUI exposure is a concern, require admin approval for new
  custom connectors, and audit Power App and Flow creation
  through the Power Platform admin activity logs.
- Assigning a blanket impact level based on a Power Platform cloud name.
  Check the specific service, supported tenant pairing, and authorization scope.

---

## ITAR posture for GCC High

**Capability.** Microsoft 365 GCC High is the established
sovereign-tenancy answer for contractors handling
ITAR-controlled technical data through productivity workflows
(email, shared documents, Teams collaboration on ITAR-scope
engineering data). Microsoft's ITAR commitments for GCC High
rest on three load-bearing claims: US data residency at the
sovereign-tenancy level (customer data and metadata reside
in the United States), US-person operator access (Microsoft
personnel with access to customer data are screened
US-persons), and contractual language in the GCC High
agreement naming ITAR support.

**CMMC practices implemented.** This posture does not map to
a specific CMMC practice; ITAR is a separate regulatory
regime. The practices affected by ITAR posture are the same
ones affected by CUI posture (access control, encryption,
audit, personnel screening) but the ITAR overlay imposes
additional constraints on contractor personnel (US-person-
only staffing where ITAR data is present) that interact with
CMMC personnel screening under PS.L2-3.9.1 and PS.L2-3.9.2.

**Implementation notes.**

- ITAR posture applies to the contractor's full ITAR
  exposure, not just the productivity suite. ITAR-controlled
  data in email, SharePoint document libraries, Teams chat,
  and OneDrive all inherit the GCC High ITAR story.
- The contractor-side personnel posture is distinct from the
  Microsoft-side posture. Microsoft guarantees US-person
  operator access; the contractor is responsible for
  ensuring contractor-side access is limited to US-persons
  where ITAR applies. A non-US-person contractor employee
  with access to an ITAR-scope SharePoint site represents a
  contractor-side violation regardless of the tenancy's
  sovereign status.
- ITAR training for contractor personnel is required;
  Microsoft does not deliver this training. Integrate ITAR
  training into the contractor's AT program (see
  `references/domains/at-awareness-training.md`).
- ITAR is different from the EAR regime. If the workload
  carries EAR-controlled dual-use data, verify the EAR posture
  separately with export-control counsel; GCC High's ITAR
  story does not automatically cover EAR.
- Cross-tenancy collaboration with non-GCC High tenants
  (commercial Microsoft 365, non-Microsoft tenants) for
  ITAR-scope content requires explicit export-control review.
  Default posture: no cross-tenant sharing of ITAR data.

**Evidence to collect.**

- Microsoft GCC High agreement and contractual ITAR language.
- Contractor ITAR policy document naming US-person staffing
  requirements for ITAR-scope work.
- Personnel screening records for staff with ITAR-scope
  access.
- Cross-tenant sharing restriction documentation.

**Common mistakes.**

- Assuming GCC High's ITAR commitment extends to the
  contractor's personnel automatically. It does not; the
  contractor owns contractor-side ITAR personnel compliance.
- Treating ITAR and EAR as interchangeable. They are distinct
  regimes with different scopes and enforcement mechanisms.
- Cross-tenant collaboration on ITAR data without
  export-control review. A single B2B guest account on an
  ITAR-scope SharePoint site can create a violation.

---

## Support and operator-access posture

**Capability.** Distinguish production operator access from support case
handling. [Microsoft's service description][ms-gcch] explicitly excludes
GCC High/DoD customer support from the service accreditation boundary
(verified 2026-10-29). A support plan does not extend that boundary.

**CMMC practices implemented.** PS.L2-3.9.1 (personnel
screening) and PS.L2-3.9.2 (personnel transfer) are inherited
from Microsoft for the Microsoft-operator side; the
contractor still owns these practices for contractor personnel.
Validate any supplier-control inheritance against the applicable package
and customer-responsibility matrix; this does not extend to ordinary support.

**Implementation notes.**

- Support cases must not include CUI data in case descriptions
  or attachments in ordinary channels. Sanitize case data and verify an
  approved channel before sharing controlled content.
- Compliance Manager and the Service Trust Portal provide
  downloadable Microsoft attestations for inherited controls.
  Use these to support SSP inheritance narrative.
- The Microsoft US-person operator-access posture applies at
  the tenancy level. Contractor personnel posture is a
  separate export-control and contract question; see ITAR
  section above.

**Evidence to collect.**

- GCC High support plan documentation per tenancy.
- Support case hygiene policy naming the CUI-scrubbing
  requirement before submission.
- Microsoft SSP sections downloaded from Service Trust Portal
  for personnel-screening inheritance.

**Common mistakes.**

- Attaching CUI logs or production data to Support cases
  without sanitization.
- Using commercial Microsoft 365 Support case URLs or
  escalation contacts for GCC High issues.

---

## FedRAMP and Impact Level posture

**Verified 2026-10-29.** Preserve the authority and scope of each statement:

| Offering | Government record observed | Microsoft description | Interpretation limit |
|---|---|---|---|
| GCC | [MSO365MT][gcc-record]: FedRAMP Certified; Rev5, Agency, Class C (Moderate) | [Government buying guide][ms-buy] and [integration guide][ms-integration] describe FedRAMP High support | The Marketplace profile and vendor description differ. Obtain the relevant High-level package/ATO evidence before asserting a High authorization for a specific service. Do not label all GCC services Moderate-only. |
| GCC High | [FR1824057433][gcch-record]: FedRAMP Certified; Rev5, Agency, Class D (High) | [Service description][ms-gcch]: FIPS 199 High assessment, IL4 equivalency or CMMC inheritance | Agency ATO path, not a GCC High JAB P-ATO. IL4 equivalency is not a DISA PA and establishes no IL5 authorization. |
| DoD | No independent DoD authorization record verified in this review | [Service description][ms-gcch]: DoD SRG IL5, purchase restricted to DoD entities | Obtain the current DoD authorization and verify eligibility, service scope, and mission-owner conditions. |

**Package identity.** MSO365MT belongs to GCC; FR1824057433 belongs to GCC
High. Microsoft's [FedRAMP overview][ms-fedramp] links to both. Older names
including Office 365 Multi-Tenant or Commercial do not extend GCC's boundary
to Commercial subscribers. Do not assign Azure's P-ATO or PA to Microsoft 365
merely because the service uses Azure infrastructure.

**Evidence limits.** This review verified public listing fields and vendor
descriptions, not restricted package contents, every service/feature, or an
independent DISA PA. Record those checks separately. If sources conflict,
retain both observations and mark the disputed claim unresolved; do not invent
an upgrade, downgrade, revocation, or blanket equivalence. FedRAMP authorization,
DoD impact-level equivalency, and CMMC certification are different determinations.

[gcc-record]: https://www.fedramp.gov/marketplace/products/MSO365MT/
[gcch-record]: https://www.fedramp.gov/marketplace/products/FR1824057433/
[ms-fedramp]: https://learn.microsoft.com/en-us/compliance/regulatory/offering-fedramp
[ms-buy]: https://learn.microsoft.com/en-us/office365/servicedescriptions/office-365-platform-service-description/office-365-us-government/microsoft-365-government-how-to-buy
[ms-gcch]: https://learn.microsoft.com/en-us/office365/servicedescriptions/office-365-platform-service-description/office-365-us-government/gcc-high-and-dod
[ms-integration]: https://learn.microsoft.com/en-us/azure/security/fundamentals/feature-availability
[ms-scope]: https://learn.microsoft.com/en-us/azure/azure-government/compliance/azure-services-in-fedramp-auditscope
[ms-comparison]: https://www.microsoft.com/en-us/microsoft-cloud/blog/us-government/2024/09/23/understanding-compliance-between-commercial-government-dod-secret-offerings-may-2026-update/

---

## Capability appendix — CMMC capability to Microsoft 365 GCC High service

Per hub Decision 1 canonical format.

| Productivity capability | Microsoft 365 GCC High service |
|---|---|
| Email | Exchange Online with Purview retention and DLP |
| File storage and collaboration | SharePoint Online + OneDrive for Business with sensitivity labels |
| Real-time messaging and chat | Microsoft Teams with information barriers and retention |
| Calendaring and meetings | Outlook Calendar + Teams Meetings |
| Document editing | Word, Excel, PowerPoint (Online and desktop) with sensitivity labels |
| Identity and access | Microsoft Entra ID Government with Conditional Access and PIM |
| Endpoint management | Microsoft Intune (GCC High) |
| DLP and sensitivity labeling | Microsoft Purview DLP, Sensitivity Labels |
| Retention and records management | Microsoft Purview Retention, Records Management |
| eDiscovery | Microsoft Purview eDiscovery Premium |
| Email security | Microsoft Defender for Office 365 Plan 2 |
| Endpoint detection and response | Microsoft Defender for Endpoint (GCC High) |
| Low-code applications | Power Platform GCC High (Power Apps, Power Automate, Power BI) |
| Audit and logging | Unified audit log via Purview; Sentinel (Azure Government) for SIEM |

---

## Cross-domain anchors

Microsoft 365 GCC High posture composes with corpus cross-
cutting files and domain practice files:

- **Phase 5d hub.** `references/modern-it/productivity/README.md`
  for the seven conventions.
- **Phase 5c cloud-platforms hub.** `references/modern-it/cloud-platforms/cloud-selection.md`
  for the FedRAMP-to-IL crosswalk under CSP SRG v1r1.
- **Azure Government platform.** `references/modern-it/cloud-platforms/azure-government.md`
  for the Azure IaaS and platform services that M365 GCC High
  sits on top of.
- **Endpoint management.** `references/modern-it/endpoints/windows-fleet.md`
  for Windows fleet management under Intune;
  `references/modern-it/endpoints/macos-fleet.md` for macOS
  under Intune.
- **FedRAMP inheritance.** `references/fedramp-gap.md`
  "Inherited vs shared-responsibility controls."
- **CUI scoping.** `references/scoping-and-cui.md`.
- **SSP authoring.** `references/ssp-guidance.md`.

Domain practice files used for requirement text and evidence
lists:

- Access Control (AC). `references/domains/ac-access-control.md`
- System and Information Integrity (SI).
  `references/domains/si-system-information-integrity.md`
- System and Communications Protection (SC).
  `references/domains/sc-system-comms.md`
- Identification and Authentication (IA).
  `references/domains/ia-identification-auth.md`
- Configuration Management (CM).
  `references/domains/cm-configuration-mgmt.md`
- Audit and Accountability (AU).
  `references/domains/au-audit.md`
- Media Protection (MP).
  `references/domains/mp-media-protection.md`
- Awareness and Training (AT).
  `references/domains/at-awareness-training.md`
- Personnel Security (PS).
  `references/domains/ps-personnel-security.md`

---

## Examples as of 2026-04

> **Examples as of 2026-04:** Microsoft 365 GCC High services
> named in this file are platform-native and are not in scope
> for the ranked-examples convention. Where a contractor
> considers third-party alternatives for a specific capability
> (third-party SIEM instead of Sentinel, third-party EDR
> instead of Defender for Endpoint, third-party identity
> federation into Entra ID Government), those vendors should
> appear in a sidebar for the relevant capability with the
> dated Examples format from the hub's capability-versus-
> product convention. This skill does not rank vendors. Verify
> current FedRAMP Marketplace status before selecting any
> third-party service operating alongside Microsoft 365 GCC
> High.

---

## Terminology

Acronyms used in this file. Terms defined in
`references/modern-it/productivity/README.md`,
`references/modern-it/cloud-platforms/cloud-selection.md`,
`references/modern-it/endpoints/windows-fleet.md`, or previous
Phase 5 slices are not repeated here.

**DoD tenancy.** The Microsoft 365 tenancy variant reserved for
Department of Defense mission-owner workloads. Microsoft describes DoD SRG IL5;
contractors typically interact as external collaborators
rather than primary tenants.

**EOP (Exchange Online Protection).** The baseline email
filtering and anti-malware service for Exchange Online.
Defender for Office 365 extends EOP with additional threat
protection.

**MDE (Microsoft Defender for Endpoint).** Defined in
`references/modern-it/endpoints/windows-fleet.md`; same
service in GCC High as in commercial tenancies architecturally
but authorized separately and running in a distinct data
plane.

**MSO365MT / FR1824057433.** The GCC / GCC High package identifiers,
respectively. See the source-separated table above for verification limits.

**Purview.** Microsoft's unified compliance platform covering
DLP, Sensitivity Labels, Retention, Records Management,
eDiscovery, Compliance Manager, and adjacent governance
tooling. Formerly Microsoft 365 Compliance.

**Safe Attachments.** The Defender for Office 365 feature that
detonates email attachments in a sandbox before delivery.

**Safe Links.** The Defender for Office 365 feature that
rewrites email URLs for just-in-time reputation evaluation
at click time.
