# Vulnerability Exposure and Remediation Assessment

An offline, standard-library Python 3 CLI for a $150 fixed-scope review of customer-supplied evidence. The demo uses fictional assets and observations. The [example report](examples/synthetic-report.md) is ready to show as a sample.

## Run the demo

From the repository root, run these commands in order.

```sh
python3 assess.py examples/synthetic-evidence.json > examples/synthetic-report.md
cat examples/synthetic-report.md
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
```

Expect three synthetic findings, two high and one medium, with evidence for five of nine asset/check combinations. The first command regenerates the included report. The CLI writes Markdown to standard output and sends input errors to standard error with exit code 2.

## Prepare evidence

Use [the sample JSON](examples/synthetic-evidence.json) as a template. Save the normalized file as UTF-8. The input has exactly these fields.

| Field | Required contents |
| --- | --- |
| `synthetic` | JSON boolean. Use `true` for fictional evidence and `false` for authorized customer evidence. |
| `approved_assets` | One to five unique asset IDs copied from the written authorization. |
| `observations` | Array of records, each containing exactly `id`, `asset`, `check` and `present`. An empty array is valid. |

Each record uses a unique evidence `id` tied to a customer-supplied source in the analyst's private evidence index. Its `asset` must exactly match an approved asset ID. IDs are case sensitive, start with an ASCII letter or digit, and use up to 80 ASCII letters, digits, dots, hyphens or underscores. Each asset/check pair may appear once.

| `check` | Condition indicated by `present: true` | Severity |
| --- | --- | --- |
| `public_admin_access` | An administrative interface is reported as publicly reachable. | High |
| `admin_mfa_disabled` | MFA is reported as disabled for administrative access. | High |
| `unsupported_software` | In-scope software is reported as out of vendor support. | Medium |

Use `present: false` only when evidence supports absence. Leave out checks with missing, unclear or conflicting evidence. The CLI rejects an entire input containing an out-of-scope observation. The analyst confirms authorization and interprets source evidence before running the CLI. The tool checks membership in the declared scope and applies fixed rules to normalized observations.

See [the service offer](OFFER.md), [outreach drafts](OUTREACH.md), [delivery process](DELIVERY.md), and [project status](PROJECT_STATUS.md).
