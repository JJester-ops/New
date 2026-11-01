# Weekly TrustMRR run (the prompt the Monday job executes)

You are running the weekly idea scan in this repo. Do these steps in order.

1. Read `profile.yaml`, `data/blocklist.json`, `data/seen.json`.
2. Pull the 25 fastest-growing startups from TrustMRR (sorted by last-30-day
   revenue growth). Per-startup pages are available as markdown at
   `https://trustmrr.com/startup/<slug>.md`. Record ONLY numbers shown on
   TrustMRR (Stripe/Paddle/RevenueCat-verified). If a number isn't shown, use
   null — never estimate. Note the date the page reports, if any.
3. For each startup in the profile's revenue band and not blocklisted, find
   where customers come from: search Reddit, X, YouTube, Product Hunt, review
   sites, and the founder's own posts. Every channel claim needs a source URL
   in `channel_evidence`. If nothing is found, leave channels empty — say
   "unknown", don't guess.
4. Score fit 0–10 against `profile.yaml` with a one-line reason.
5. Write `data/snapshots/<today>.json` (schema in `scripts/build_report.py`),
   then run `python3 scripts/build_report.py data/snapshots/<today>.json`.
6. For the top NEW winner, write `reports/<today>-steal-sheet.md` using
   `templates/steal-sheet.md`.
7. Commit `data/` and `reports/` and push.

Ground rules: revenue ≠ profit; a 30-day window can be a one-off spike;
"steal" means copy the demand pattern, not the brand, code, or content.
