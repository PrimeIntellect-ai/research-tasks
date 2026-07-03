You are an infrastructure engineer working as a capacity planner for our microservices deployment. You need to fix a broken storage monitoring pipeline, automate an interactive backup, and create a security sanitizer for our log processor.

Here are your tasks:

1. **Docker Compose Network Fix**
   We have a monitoring stack defined in `/home/user/capacity-stack/docker-compose.yml`. Currently, the `log_aggregator` service cannot reach the `db` service due to a network misconfiguration (they are on mismatched, isolated networks). Modify the `docker-compose.yml` file so that both services successfully communicate on a single bridge network named `capacity_net`. 

2. **Automate Interactive Backup**
   Our storage system requires daily backups using an interactive tool located at `/app/interactive_backup.sh`. This tool does not accept command-line flags. You must write a Python script using `pexpect` (or a bash script using `expect`) at `/home/user/run_backup.py` that automates this tool. 
   When executed, the tool prompts exactly:
   - `Initiate backup? (y/n):` -> you must answer `y`
   - `Target volume:` -> you must answer `metrics_db`
   - `Max quota (GB):` -> you must answer `500`
   Your script should run the tool to completion and save the resulting backup archive to `/home/user/backups/latest.tar.gz` (the tool automatically drops it in the current working directory as `backup.tar.gz`, so you must move it).

3. **Adversarial Log Sanitizer**
   Our downstream log processor, `/app/capacity_monitor` (a stripped binary), is vulnerable to malicious capacity payloads that spoof disk quotas or crash the service. 
   You must write a Python classifier at `/home/user/sanitize.py` that takes a single file path as a command-line argument:
   `python3 /home/user/sanitize.py <path_to_json_log>`
   
   The script must exit with status `0` if the log file is perfectly clean and valid, and exit with status `1` if it is malicious ("evil").
   
   To help you develop this, we have provided two directories of sample logs:
   - `/app/corpora/clean/` : Contains valid JSON logs.
   - `/app/corpora/evil/` : Contains malicious JSON logs.
   
   You can also test logs against the black-box oracle `/app/capacity_monitor <path_to_log>`. By observing how the stripped binary behaves (e.g., successfully printing the calculated storage vs. crashing, returning errors, or exposing negative quotas), you should deduce the characteristics of "evil" files. Implement those checks in your `sanitize.py` script.

Ensure all scripts are executable and placed exactly at the paths specified.