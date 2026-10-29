# Claim review for SSP use (2026-09-29)

This is a targeted review of claims that the evaluation scenarios previously
treated as fixed answers. It is not a certification of the full reference
corpus. Before an SSP cites a product or authorization claim, record the
contract requirement, exact offering, feature, region, model if relevant,
authorization boundary, primary URL, and review date. Obtain the current
package scope from the authorizing record; a vendor summary alone is not
an authorization letter or an inheritance determination.

| Old claim or grading assumption | Review finding | Primary source checked |
|---|---|---|
| DFARS 252.204-7012 plus CUI always requires Level 2 C3PAO | Unsupported. The CMMC level and assessment type are specified through the CMMC acquisition provisions and contract. Check the actual solicitation, clause, and flow-down. | [DFARS 204.7503](https://www.acquisition.gov/dfars/subpart-204.75-cybersecurity-maturity-model-certification); [DFARS 252.204-7021](https://www.acquisition.gov/dfars/252.204-7021-contractor-compliance-cybersecurity-maturity-model-certification-level-requirements.); [DFARS 252.204-7012](https://www.acquisition.gov/dfars/252.204-7012-safeguarding-covered-defense-information-and-cyber-incident-reporting.) |
| Office 365 GCC is categorically FedRAMP Moderate and GCC High is IL5 | Contradicted by Microsoft's current descriptions. Office 365 GCC supports FedRAMP High. GCC High can demonstrate IL4 equivalency or CMMC inheritance; Microsoft describes Office 365 DoD as DoD SRG IL5 certified. Service-specific scope and conditions still need verification. | [Microsoft cloud feature availability](https://learn.microsoft.com/en-us/azure/security/fundamentals/feature-availability); [GCC High and DoD service descriptions](https://learn.microsoft.com/en-us/office365/servicedescriptions/office-365-platform-service-description/office-365-us-government/gcc-high-and-dod) |
| GCC uses Entra ID Government | Microsoft's current integration description says Office 365 GCC pairs with Entra ID in Azure, while GCC High and DoD pair with Entra ID in Azure Government. | [Microsoft cloud feature availability](https://learn.microsoft.com/en-us/azure/security/fundamentals/feature-availability) |
| GitHub Copilot Enterprise has a fixed Azure OpenAI Government backend and CUI source code is automatically acceptable | Unsupported by the current GitHub policy documentation. GitHub describes a policy for US data residency enterprises to restrict Copilot to FedRAMP Moderate models; it is disabled by default. This does not establish the authorization of every data path or CUI workflow. | [GitHub FedRAMP-compliant models](https://docs.github.com/en/copilot/concepts/enterprise/fedramp-models) |
| A fixed April 2026 Bedrock model list and blanket IL4/IL5 assertion are current | AWS maintains a model-specific FedRAMP and DoD SRG matrix, updated August 25, 2026 in the checked page. Verify the model, region, and service status for each deployment. | [AWS Bedrock model certification matrix](https://aws.amazon.com/compliance/services-in-scope/FedRAMP/amazon-bedrock-models/) |

Cursor routing, Claude Code telemetry and backend details, FedRAMP package
identifiers, other vendor entries in the productivity table, and the many
remaining `verified 2026-04-21` assertions were **not** independently
revalidated in this review. Treat them as historical context. The scenario
graders no longer require the unverified product assertions. The skill now
requires fresh primary-source checks before SSP-facing use.

## Microsoft follow-up (2026-10-29)

The September warning is now reconciled through the distributed corpus and
structured snapshot. [GCC MSO365MT](https://www.fedramp.gov/marketplace/products/MSO365MT/)
currently shows Class C (Moderate), Agency path; [GCC High FR1824057433](https://www.fedramp.gov/marketplace/products/FR1824057433/)
shows Class D (High), Agency path. Both show FedRAMP Certified. Microsoft still
describes GCC High-level support. Preserve that difference; neither a blanket
Moderate-only claim nor an independently verified GCC High-level listing follows.
GCC High's vendor IL4 equivalency is distinct from a DoD PA. See the October
source register and `microsoft-365-gcc.md` for service and contract checks.
Only these Microsoft entries and related cross-references were revalidated;
other vendor claims retain their prior verification limits.
