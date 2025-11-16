Community outreach optimisation 

Streamlines outreach to community prospects which we use internally for AI/ML events.

Why this exists

Native outreach tooling is limited. This script saves time assisting us to send personalised outreach campaigns.
…

Tip: Use the CSV with Outlook/Word Mail Merge, your sequencer, or your CRM—always respecting opt-outs and your data policy.

Prerequisites

Python 3.9+

Playwright (pip install playwright) and browsers (playwright install)

A Chromium-based browser launched with remote debugging enabled

Quick start

Launch your browser with DevTools port (e.g., 9222)
Windows:

"C:\Program Files\Google\Chrome\Application\chrome.exe" ^
  --remote-debugging-port=9222 --user-data-dir="C:\temp\devtools" ^
  --disable-extensions --no-first-run


macOS:

/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 --user-data-dir="/tmp/devtools" \
  --disable-extensions --no-first-run


Log in to your ATS and open the Prospects list (or People → Applications).

Run the script:

python3 email-scraper


Open prospect_emails.csv.

Configuration (optional)

CDP_URL – DevTools endpoint (default http://127.0.0.1:9222)

OUTPUT_CSV – output file name

Concurrency and timeouts (tune inside the script)

Limitations & notes

Only emails visible to your account are captured.

Very large lists: increase concurrency modestly and monitor rate limits.

The script does not perform login; it relies on your already-open, authenticated tab.

Troubleshooting

“No suitable tab found” → Ensure the Prospects list is open in the same browser instance started with --remote-debugging-port=9222.

Zero emails → Inspect the profile DOM and add a selector for the personal-info block if needed.

Timeouts → Raise per-page timeout or lower concurrency.

Compliance & data use

Ensure a lawful basis for processing personal data (e.g., legitimate interests) and comply with UK/EU GDPR where applicable.

Honour opt-outs/suppression lists and your company privacy policy.

Store the CSV securely and limit access to authorised team members only.


