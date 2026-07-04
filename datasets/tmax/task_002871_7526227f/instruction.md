You are tasked with fixing a reporting script for our mail server's alias management system. 

We have a "cron-like" job that runs a Python script to process an email aliases configuration file and generate a report. However, the script is currently failing or writing to the wrong locations because the job runner executes it from a different working directory (`/tmp`). Additionally, the script crashes if it encounters malformed lines in the configuration file.

The relevant files are located in `/home/user/mail_manager/`:
- `run_job.sh`: A wrapper script simulating the scheduled job runner. Do not modify this file.
- `generate_report.py`: The Python script that reads the config and generates a report.
- `config/aliases.conf`: The configuration file containing email aliases.

Your objectives:
1. **Fix Path Issues:** Modify `/home/user/mail_manager/generate_report.py` so that it always reads exactly from `/home/user/mail_manager/config/aliases.conf` and writes its output to `/home/user/mail_manager/report.log`, regardless of the current working directory it is executed from. Do not use relative paths like `config/aliases.conf` directly.
2. **Add Robust Error Handling:** Update the Python script to gracefully handle malformed lines in the configuration file. Valid lines have exactly one colon (`:`) separating the alias and the email address. Ignore blank lines and lines starting with `#`. If a line is malformed (missing a colon or having too many), the script should NOT crash. Instead, it should skip the alias and write the exact string `ERROR: Malformed line - <exact raw line>` to the output log.
3. **Fix the Config File:** Inspect `/home/user/mail_manager/config/aliases.conf`. The `marketing` alias is missing a colon. Fix this specific line in the configuration file so it properly maps `marketing` to `marketing@example.com`. 
4. **Leave the Intentional Error:** There is another malformed line for `devops` in the config file. **Do not fix the `devops` line.** Leave it broken so that we can verify your script's error handling.

The final output in `/home/user/mail_manager/report.log` should contain the valid aliases in the format `<alias> -> <email>` (stripped of surrounding whitespace) and the error messages for any malformed lines. 

Verify your solution by running `/home/user/mail_manager/run_job.sh` and ensuring `/home/user/mail_manager/report.log` is generated correctly.