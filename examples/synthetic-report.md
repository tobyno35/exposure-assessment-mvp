# Vulnerability Exposure and Remediation Assessment

**Synthetic demonstration. All assets, evidence and findings below are fictional.**

## Summary

Saved evidence indicates **3 exposure findings** (2 high, 1 medium).
Evidence was supplied for **5 of 9** asset/check combinations.

High findings are prioritized for review because they concern administrative access. Medium findings call for planned remediation. Severity reflects the condition reported in the evidence and may change with business context.

## Approved scope

- `demo-gateway`
- `demo-admin-portal`
- `demo-file-server`

## Findings and remediation

### Synthetic finding 1 — MFA is reported as disabled for administrative access

- **Severity** — High
- **Asset** — `demo-admin-portal`
- **Evidence reference** — `DEMO-04`
- **Recommended action** — Require MFA for administrative accounts and review recovery and break-glass access.

### Synthetic finding 2 — Administrative access is reported as publicly reachable

- **Severity** — High
- **Asset** — `demo-gateway`
- **Evidence reference** — `DEMO-01`
- **Recommended action** — Review business need and restrict administrative access to approved networks or a managed private access service.

### Synthetic finding 3 — Software is reported as out of support

- **Severity** — Medium
- **Asset** — `demo-file-server`
- **Evidence reference** — `DEMO-05`
- **Recommended action** — Confirm lifecycle status with the vendor and plan an upgrade or replacement.

## Evidence and coverage

Evidence IDs refer to observations in the saved input. A missing observation means evidence was not supplied for that check.

| Asset | Check | Evidence ID | Reported condition |
| --- | --- | --- | --- |
| `demo-gateway` | `public_admin_access` | `DEMO-01` | Present |
| `demo-gateway` | `admin_mfa_disabled` | `DEMO-02` | Absent |
| `demo-gateway` | `unsupported_software` | — | No evidence supplied |
| `demo-admin-portal` | `public_admin_access` | `DEMO-03` | Absent |
| `demo-admin-portal` | `admin_mfa_disabled` | `DEMO-04` | Present |
| `demo-admin-portal` | `unsupported_software` | — | No evidence supplied |
| `demo-file-server` | `public_admin_access` | — | No evidence supplied |
| `demo-file-server` | `admin_mfa_disabled` | — | No evidence supplied |
| `demo-file-server` | `unsupported_software` | `DEMO-05` | Present |

## Method and limitations

This report applies fixed rules to supplied observations. Scope is checked against the asset IDs listed in the input. The review uses no live testing and provides no independent verification of the observations or completeness of the customer's security controls.
