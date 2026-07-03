You are an on-call engineer responding to a 3 AM PagerDuty alert. The automated billing processor is failing to generate the nightly summary file.

System context:
- The entry point is `/home/user/billing/run.sh`.
- The main processor script is `/home/user/billing/processor.py`.
- The data is located at `/home/user/billing/transactions.log`.

Symptoms reported:
1. When cron executes `/home/user/billing/run.sh`, the process hangs forever, consuming 100% CPU on a single core. It never completes or outputs anything.
2. The expected output file `/home/user/billing_summary.txt` is missing.

Your investigation notes so far:
- The previous engineer deployed a rushed patch yesterday, and it appears some files might have been accidentally deleted or misconfigured in the `/home/user/billing` directory.
- The system timezone or environment configurations might have been tampered with.
- The upstream log aggregator warned us that some raw log files (like `transactions.log`) might contain data corruption, such as injected null bytes (`\x00`), which the script must gracefully handle or strip.

Your objective:
1. Diagnose and fix the root cause of the infinite hang in `processor.py`.
2. Fix any environment misconfigurations preventing proper timezone handling.
3. Recover any accidentally deleted configuration files required by the script.
4. Ensure the script handles corrupted data without getting stuck.
5. Successfully execute `/home/user/billing/run.sh` to produce `/home/user/billing_summary.txt`.

The final `billing_summary.txt` should contain exactly one line with the calculated floating-point total.