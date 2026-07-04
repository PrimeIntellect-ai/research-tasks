You are assisting a FinOps analyst in setting up an automated daily cost aggregation script on a cloud VM. The analyst wants a custom C++ application to run daily under a specific timezone and environment configuration.

Perform the following tasks:

1. **Write and Compile a C++ Utility**:
   Create a C++ program at `/home/user/cost_monitor.cpp`. The program must:
   - Include `<iostream>` and `<cstdlib>`.
   - Read the environment variable `FINOPS_TIER`. If it is not set, default to `"standard"`.
   - Print exactly this format to standard output: `[<TIER>] Cost computation triggered.` (replace `<TIER>` with the value of the environment variable).
   - Compile this program to an executable named `/home/user/cost_monitor` using `g++`.

2. **Environment Configuration**:
   The analyst needs the monitoring environment to consistently use the Auckland timezone and a specific tier.
   Append the following environment variable exports to `/home/user/.bashrc`:
   - Set `TZ` to `Pacific/Auckland`.
   - Set `FINOPS_TIER` to `enterprise`.

3. **Scheduled Task Setup**:
   Configure the user's crontab so that `/home/user/cost_monitor` executes exactly at 23:45 (11:45 PM) every day.
   After installing the crontab, run `crontab -l > /home/user/cron_verify.txt` so the automated system can verify your cron configuration.

Ensure all file paths are exact and the C++ program compiles successfully without warnings or errors.