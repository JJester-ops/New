# TrustMRR idea scanner

Each week, check TrustMRR's fastest-growing *verified-revenue* startups, filter them to
businesses one person could run, rank new ones first, and write a steal sheet for the top one.

- `profile.yaml`: the kind of business you'd run (fill in the TODOs)
- `data/blocklist.json`: ideas you said no to, which never come back
- `WEEKLY_RUN.md`: the exact instructions the scheduled job follows
- `scripts/build_report.py`: snapshot JSON → `reports/<date>.xlsx` + `.md`
- `templates/steal-sheet.md`: demand / offer / channels / angle / 7-day test

Runs as a Claude Code cloud scheduled task, so it doesn't depend on a laptop being awake.
