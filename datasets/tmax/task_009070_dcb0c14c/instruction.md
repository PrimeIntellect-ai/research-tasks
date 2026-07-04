You are a Site Reliability Engineer (SRE) investigating an issue with your team's custom uptime calculation service. 

The service is written in Go and processes a JSONL log file of simulated minute-by-minute ping results to calculate two metrics for a specific time window:
1. The longest contiguous downtime (in minutes).
2. The overall uptime percentage for the queried window.

Currently, the service in `/home/user/uptime_calculator/main.go` has two severe bugs:
1. When you run it, it crashes with a panic and dumps a stack trace. You need to analyze the stack trace to find and fix the off-by-one boundary error causing the crash.
2. The uptime query result is inaccurate. The SRE team requires the time window filter (from `startTS` to `endTS`) to be **inclusive** of both boundaries, but the current query logic is skipping the final minute's data.

Your task:
1. Navigate to `/home/user/uptime_calculator/`.
2. Run the `main.go` program and analyze the resulting stack trace to fix the panic (array bounds issue).
3. Fix the logical boundary condition error so that the queried time window includes the `endTS` timestamp.
4. Run the fixed program. It is designed to automatically write its results to `/home/user/uptime_report.json`.

Ensure the final JSON file at `/home/user/uptime_report.json` strictly contains the corrected results in this format:
`{"longest_downtime_minutes": X, "uptime_percentage": Y.YY}`