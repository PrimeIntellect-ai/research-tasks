You are an automation specialist responsible for establishing a secure time-series log processing pipeline.

We have a legacy tool designed to tokenize and mask sensitive data in time-series logs (like API keys and SSNs). The source code for this tool is vendored at `/app/log-masker-1.0.0/`. However, the build system for this tool is currently broken due to a configuration error.

Your objectives are:

1. **Fix the Vendored Package**: Inspect and fix the build process for the `log-masker` tool in `/app/log-masker-1.0.0/`. Compile it so that the executable `masker` is successfully generated in that directory.
2. **Develop a Processing Pipeline**: Create a shell script at `/home/user/pipeline.sh` that takes exactly two arguments:
   `./pipeline.sh <input_log_file> <output_log_file>`
   This script must use the fixed `masker` tool to process the input file and write the sanitized logs to the output file. 
3. **Adversarial Validation**: We have provided two corpora of logs for you to test your pipeline against:
   - `/home/user/corpus/clean/`: Contains normal time-series metrics. These must remain *exactly* unchanged.
   - `/home/user/corpus/evil/`: Contains logs with embedded PII (`api_key=[32-chars]` and `ssn=[9-digits]`). Your pipeline MUST redact these values to `[REDACTED]`.
   Make sure your script perfectly processes these before proceeding.
4. **Schedule the Pipeline**: Set up a user cron job (using `crontab`) that executes `/home/user/cron_runner.sh` exactly every 5 minutes. You must create `/home/user/cron_runner.sh` to find all `.log` files in `/home/user/incoming/`, process them using `/home/user/pipeline.sh`, save the sanitized output to `/home/user/outgoing/` (keeping the same filenames), and then delete the original files from `/home/user/incoming/`.

Ensure all scripts are executable and that the cron job is correctly installed for the `user` account.