You are acting as a FinOps analyst trying to optimize cloud storage costs. We have a custom monitoring tool written in C that parses a mock `fstab`-like configuration file containing cloud volumes and their current monthly costs. If a volume's cost exceeds $100, it writes an alert to a log file.

However, the tool is currently crashing (Segmentation Fault) because it fails to properly handle empty lines and comments in the configuration file. 

Your tasks:
1. Fix the bug in the C program located at `/home/user/finops_monitor.c`. The program should safely ignore empty lines and lines starting with `#`. 
2. Compile the fixed C program to `/home/user/finops_monitor` using `gcc`.
3. Run the compiled executable once. It should read `/home/user/cloud_fstab` and create `/home/user/cost_alerts.log`.
4. Schedule this script to run every 5 minutes by adding a cron job for the current user. The crontab entry should execute the absolute path `/home/user/finops_monitor`.

**System State & Formats:**
- The source file `/home/user/finops_monitor.c` and configuration file `/home/user/cloud_fstab` already exist.
- The output file `/home/user/cost_alerts.log` must be created by the C program.
- Do not modify `/home/user/cloud_fstab`.
- The crontab must be successfully installed using the `crontab` command.