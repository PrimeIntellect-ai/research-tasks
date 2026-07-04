You are a capacity planner analyzing resource usage for a fleet of simulated applications. You need to write a Go program to aggregate process metrics, map them to their deployment environments using directory symlinks, format a localized email report, and generate a process control script.

The system has been set up with the following structure:
- `/home/user/deployments/` contains directories representing environments (e.g., `prod`, `dev`).
- `/home/user/apps/` contains application directories. Inside each app directory (e.g., `/home/user/apps/app1`), there is a symlink named `env` that points to its corresponding environment directory in `/home/user/deployments/`.
- `/home/user/mock_metrics/` contains JSON files named `<pid>.json`. Each file represents a running process and contains data in this format: `{"pid": 1001, "app": "app1", "memory_mb": 800, "cpu_percent": 60.5}`.

Your task is to write and execute a Go program at `/home/user/analyzer.go` that does the following:

1. **Process Analysis and Directory Resolution:**
   Read all JSON files in `/home/user/mock_metrics/`. For each process, look up its `app` name in `/home/user/apps/<app_name>/env`. Read the symlink to determine which deployment environment the app belongs to (the environment name is the base name of the target directory, e.g., `prod`).

2. **Metric Aggregation:**
   Calculate the total `memory_mb` and total `cpu_percent` used by all processes in each environment.

3. **Process Control:**
   Generate a bash script at `/home/user/kill_high_cpu.sh`. For every process where `cpu_percent > 50.0`, append a command to this script to kill it forcefully: `kill -9 <pid>`. Ensure the script has an executable shebang `#!/bin/bash` and make the file executable (`chmod +x`).

4. **Email Report Generation with Timezones:**
   The Go program must accept a single command-line argument: a Unix epoch timestamp (e.g., `1729663200`). 
   It must convert this timestamp to the `Asia/Tokyo` timezone and generate an RFC 5322 formatted email file at `/home/user/capacity_report.eml`.

The email file must exactly match this format:
```
To: admin@example.com
From: planner@example.com
Subject: Capacity Report
Date: <Formatted Date>

Environment: <env1>
Total Memory: <total_mem> MB
Total CPU: <total_cpu>%

Environment: <env2>
Total Memory: <total_mem> MB
Total CPU: <total_cpu>%
```

**Formatting Rules:**
- The `<Formatted Date>` must use the standard RFC 5322 format but localized to the `Asia/Tokyo` timezone (e.g., `Wed, 23 Oct 2024 15:00:00 +0900`).
- Environments must be sorted alphabetically in the report.
- CPU percentages must be formatted to exactly one decimal place (e.g., `115.5%` or `10.0%`).
- Separate the headers from the body with a single blank line.
- Separate each Environment block with a single blank line.

Build and run your Go program using the timestamp `1729663200`. Leave the resulting `/home/user/capacity_report.eml` and `/home/user/kill_high_cpu.sh` on the disk for verification.