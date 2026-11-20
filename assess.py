"""Generate an offline exposure assessment from saved evidence."""

import argparse
import json
import re
from pathlib import Path


# Each rule describes a reported condition and a suggested remediation.
RULES = {
    "public_admin_access": (
        "High",
        "Administrative access is reported as publicly reachable",
        "Review business need and restrict administrative access to approved networks "
        "or a managed private access service.",
    ),
    "admin_mfa_disabled": (
        "High",
        "MFA is reported as disabled for administrative access",
        "Require MFA for administrative accounts and review recovery and break-glass access.",
    ),
    "unsupported_software": (
        "Medium",
        "Software is reported as out of support",
        "Confirm lifecycle status with the vendor and plan an upgrade or replacement.",
    ),
}


def require_fields(value, fields, label):
    if not isinstance(value, dict) or value.keys() != set(fields):
        raise ValueError(f"{label} must contain exactly these fields: {', '.join(fields)}")


def identifier(value, label):
    if not isinstance(value, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,79}", value):
        raise ValueError(f"{label} must be an identifier using 1–80 letters, digits, dots, hyphens, or underscores")
    return value


def unique_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("JSON contains a duplicate object key")
        result[key] = value
    return result


def load_evidence(path):
    data = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_keys)
    require_fields(data, ("synthetic", "approved_assets", "observations"), "Evidence")
    if type(data["synthetic"]) is not bool:
        raise ValueError("synthetic must be a JSON boolean")

    assets = data["approved_assets"]
    if not isinstance(assets, list) or not 1 <= len(assets) <= 5:
        raise ValueError("approved_assets must be a list of 1–5 asset IDs")
    for asset in assets:
        identifier(asset, "Approved asset")
    if len(set(assets)) != len(assets):
        raise ValueError("Approved asset IDs must be unique")

    observations = data["observations"]
    if not isinstance(observations, list):
        raise ValueError("observations must be a list")
    seen_ids = set()
    seen_checks = set()
    for index, row in enumerate(observations, 1):
        label = f"Observation {index}"
        require_fields(row, ("id", "asset", "check", "present"), label)
        evidence_id = identifier(row["id"], f"{label} ID")
        asset = identifier(row["asset"], f"{label} asset")
        if asset not in assets:
            raise ValueError(f"{label} references an asset outside the approved scope")
        check = row["check"]
        if not isinstance(check, str) or check not in RULES:
            raise ValueError(f"{label} has an unsupported check")
        if type(row["present"]) is not bool:
            raise ValueError(f"{label} present must be a JSON boolean")
        if evidence_id in seen_ids or (asset, check) in seen_checks:
            raise ValueError(f"{label} repeats an evidence ID or asset/check pair")
        seen_ids.add(evidence_id)
        seen_checks.add((asset, check))
    return data


def render_report(data):
    synthetic = data["synthetic"]
    assets = data["approved_assets"]
    rows = data["observations"]
    findings = sorted(
        (row for row in rows if row["present"]),
        key=lambda row: (RULES[row["check"]][0] != "High", row["asset"], row["check"]),
    )
    high = sum(RULES[row["check"]][0] == "High" for row in findings)
    total_checks = len(assets) * len(RULES)
    lines = ["# Vulnerability Exposure and Remediation Assessment", ""]
    if synthetic:
        lines += [
            "**Synthetic demonstration. All assets, evidence and findings below are fictional.**",
            "",
        ]
    lines += [
        "## Summary",
        "",
        f"Saved evidence indicates **{len(findings)} exposure findings** "
        f"({high} high, {len(findings) - high} medium).",
        f"Evidence was supplied for **{len(rows)} of {total_checks}** "
        "asset/check combinations.",
        "",
        "High findings are prioritized for review because they concern administrative access. "
        "Medium findings call for planned remediation. Severity reflects the condition "
        "reported in the evidence and may change with business context.",
        "",
        "## Approved scope",
        "",
    ]
    lines.extend(f"- `{asset}`" for asset in assets)
    lines += ["", "## Findings and remediation", ""]
    if not findings:
        lines += ["The supplied evidence reported none of the supported exposure conditions.", ""]
    for index, row in enumerate(findings, 1):
        severity, title, remediation = RULES[row["check"]]
        prefix = "Synthetic finding" if synthetic else "Finding"
        lines += [
            f"### {prefix} {index} — {title}",
            "",
            f"- **Severity** — {severity}",
            f"- **Asset** — `{row['asset']}`",
            f"- **Evidence reference** — `{row['id']}`",
            f"- **Recommended action** — {remediation}",
            "",
        ]
    lines += [
        "## Evidence and coverage",
        "",
        "Evidence IDs refer to observations in the saved input. "
        "A missing observation means evidence was not supplied for that check.",
        "",
        "| Asset | Check | Evidence ID | Reported condition |",
        "| --- | --- | --- | --- |",
    ]
    by_check = {(row["asset"], row["check"]): row for row in rows}
    for asset in assets:
        for check in RULES:
            row = by_check.get((asset, check))
            if row is None:
                lines.append(f"| `{asset}` | `{check}` | — | No evidence supplied |")
            else:
                status = "Present" if row["present"] else "Absent"
                lines.append(f"| `{asset}` | `{check}` | `{row['id']}` | {status} |")
    lines += [
        "",
        "## Method and limitations",
        "",
        "This report applies fixed rules to supplied observations. Scope is checked "
        "against the asset IDs listed in the input. The review uses no live testing "
        "and provides no independent verification of the observations or completeness "
        "of the customer's security controls.",
        "",
    ]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("evidence", type=Path, help="saved JSON evidence file")
    args = parser.parse_args()
    try:
        report = render_report(load_evidence(args.evidence))
    except (OSError, ValueError, RecursionError) as error:
        parser.exit(2, f"Assessment rejected: {error}\n")
    print(report, end="")


if __name__ == "__main__":
    main()
