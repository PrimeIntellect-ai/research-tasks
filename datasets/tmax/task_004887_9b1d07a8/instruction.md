You are a FinOps analyst tasked with optimizing our simulated cloud cost reporting pipeline. We have a local microservices architecture that generates usage logs, aggregates them, and sends them to a mock billing API. Currently, our bill is too high because we are sending non-billable metrics to the billing API, and the pipeline is fragile.

Your objectives:

1. **Fix the Process Supervision (Systemd)**:
   There are three user-level systemd services located in `/home/user/.config/systemd/user/`:
   - `billing-receiver.service` (listens on port 8080)
   - `log-generator.service` (generates usage logs to `/home/user/app/usage.log`)
   - `cost-aggregator.service` (reads the log file and sends data to the billing receiver)
   
   Currently, `cost-aggregator.service` fails to start on boot because it tries to connect to the receiver before it is ready. Fix `cost-aggregator.service` by adding the correct `After=` and `Requires=` dependencies so it waits for `billing-receiver.service`. Also, configure it so that it automatically restarts on failure (`Restart=always`, `RestartSec=5`). Reload the systemd user daemon and ensure all three services are running successfully.

2. **Develop the Cost Optimization Filter (Adversarial Corpus)**:
   We are sending "dev", "test", and zero-cost metrics to the billing provider, which charges us per data point! You must write a filter script (in any language you choose, e.g., Bash, Python, awk) at `/home/user/cost-filter`. Make sure it is executable (`chmod 700 /home/user/cost-filter`).
   
   This script must read JSON-lines from standard input (`stdin`) and write strictly the allowed JSON-lines to standard output (`stdout`). 
   - **Reject (Evil)**: Any JSON line where the `"env"` field is `"dev"` or `"test"`, OR where the `"cost"` field is exactly `0` (or missing/null).
   - **Keep (Clean)**: Any JSON line where `"env"` is `"prod"` AND `"cost"` is strictly greater than `0`.
   
   You can test your filter against our offline corpora. The clean metrics are in `/home/user/app/corpora/clean/` and the wasteful metrics are in `/home/user/app/corpora/evil/`. An automated test will pipe these files into your script. Your script must preserve 100% of the clean corpus and reject (output nothing for) 100% of the evil corpus.

3. **Pipeline Integration**:
   The `cost-aggregator.service` executes a wrapper script at `/home/user/app/run-aggregator.sh`. Modify this bash script so that the `tail -F /home/user/app/usage.log` command is piped through your new `/home/user/cost-filter` before being passed to the `send-to-billing` command. 

4. **Verification Environment**:
   Write the exact absolute path to your filter script into `/home/user/solution.env` like so:
   `FILTER_CMD="/home/user/cost-filter"`
   
   Ensure all systemd user services are running and functioning end-to-end. The test will verify both the corpora pass rates and the live end-to-end flow using systemctl status and API counts.