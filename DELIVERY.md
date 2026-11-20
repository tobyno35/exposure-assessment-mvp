# Customer delivery

## Intake and written authorization

1. Ask who can authorize the review and who should receive the report. Identify up to five systems, assign stable asset IDs, and agree which of the three checks each submitted artifact can support. Confirm a private transfer method and a deletion date with the customer.
2. Obtain written approval from the authorized representative before reviewing evidence. Save it with the job record. Use this approval text and fill in all placeholders.

   > I, [name and role], confirm I am authorized to approve this review for [business]. I authorize [provider] to review saved evidence supplied by our business for these systems and asset IDs [list]. The $150 assessment covers evidence review and a Markdown report. It excludes live access and testing. Please send the report to [recipient] via [agreed channel] and delete the evidence by [date]. Delivery is due within three business days of this approval and receipt of the agreed evidence.

3. Request dated, redacted screenshots or saved exports showing relevant administrative access settings, MFA requirements, or software lifecycle information. Ask the customer to omit passwords, keys, tokens and personal data. Use the agreed transfer channel. Confirm receipt of the agreed evidence and the delivery date.

## Review checklist

- Match each artifact to the approved asset ID. Set aside material for any unapproved system and ask the customer for a corrected submission or updated written authorization before reviewing it.
- Assign an evidence ID and record the asset, source filename or screenshot reference, capture date, relevant setting, and interpretation in a private evidence index. Keep the index and customer evidence outside the demo repository.
- Use a positive or negative observation only when the artifact supports that conclusion for the specific asset and check. Leave unsupported, stale or conflicting observations out of the JSON and note material gaps in the handoff.
- Copy the approved IDs into the JSON, set `synthetic` to `false` for customer evidence, and run the CLI. Review the report against the private evidence index. Check the finding count, severity, scope, coverage gaps, and action wording. Keep conclusions qualified as evidence-based observations. Add customer-specific priorities only where the evidence and business context support them.

## Handoff

Send the Markdown report to the agreed recipient through the agreed channel. In the handoff, summarize the highest-priority actions, call out gaps that affect decisions, and identify which actions the customer or their IT provider can take. Include a shareable mapping of evidence IDs to the customer's source filenames or screenshot locations so the customer can trace each finding. Keep raw artifacts out of the handoff unless the customer requests them through the agreed channel.

Offer one round of email clarification within seven calendar days of delivery. Record the delivery and remove the supplied evidence, normalized JSON and private evidence index according to the agreed retention terms.
