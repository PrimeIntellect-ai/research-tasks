You are a Site Reliability Engineer (SRE) configuring a new uptime monitoring tool. The tool calculates maximum allowable downtime to maintain strict SLAs, utilizing a fast C-extension for metric penalties and a Python script for the iterative calculation.

The tool is located in `/home/user/uptime_monitor`. Currently, the system is broken in two ways:
1. **Build Failure**: Running `make` in the directory fails to compile the required shared library.
2. **Convergence & Precision Failure**: Once the library is built, running `python /home/user/uptime_monitor/calculate_sla.py` fails to converge. The script attempts to iteratively calculate a downtime budget that precisely hits a target SLA of `0.99999`. However, due to floating-point precision issues and an exact equality check, it loops until it hits a safeguard limit and crashes.

Your tasks:
1. Diagnose and fix the build failure in the `Makefile` so that `make` successfully produces `libmetrics.so`.
2. Fix the convergence logic in `calculate_sla.py` by replacing the exact equality check with a proper floating-point tolerance check (use a tolerance of `1e-9` for the absolute difference between `current_sla` and `target_sla`).
3. Run `python calculate_sla.py` to generate the output log.

The script, once fixed and run, will automatically write its results to `/home/user/uptime_monitor/sla_report.txt`. Ensure this file is created successfully.