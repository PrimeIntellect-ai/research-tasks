You are a backup operator testing the restore process of a custom mailing list server configuration in a staged deployment environment. 

You need to automate the configuration of a restored interactive setup tool, ensure the deployment script is idempotent, and write a C program to verify the restored email spools.

Here are your specific tasks:

1. **Automate Interactive Setup via Expect:**
   There is an interactive configuration tool located at `/home/user/bin/interactive_setup` (already existing). When executed, it interactively prompts for three pieces of information, one by one:
   - "Enter Admin Email: "
   - "Enter SMTP Port: "
   - "Enter Deployment Stage (staging/prod): "
   
   Write an Expect script at `/home/user/setup_mailer.exp` that automates this tool. It should feed the tool the following values:
   - Admin Email: `admin@backup.local`
   - SMTP Port: `2525`
   - Stage: `staging`
   The tool will automatically generate a configuration file at `/home/user/mailer_config.txt` in the format `key=value`.

2. **Idempotent Deployment Script:**
   Write a Bash script at `/home/user/deploy.sh` that acts as an idempotent deployment wrapper. 
   - When executed, it should check if `/home/user/mailer_config.txt` already exists AND contains `STAGE=staging`. 
   - If it does, the script should output "Configuration already applied." and exit with code 0 without running the expect script.
   - If it does not exist or has a different stage, it should run `/home/user/setup_mailer.exp` to configure it.
   - Run your `deploy.sh` script to generate the config file.

3. **Verify Restored Spool via C Program:**
   The restored email spool is located in the directory `/home/user/spool/`. It contains several text files representing raw emails.
   Write a C program at `/home/user/check_spool.c` that does the following:
   - Reads `/home/user/mailer_config.txt` to extract the `ADMIN`, `PORT`, and `STAGE` values.
   - Scans the directory `/home/user/spool/` for files.
   - Reads each file in the spool and counts the number of "valid" emails. An email is considered valid if it contains the exact string `To: list@backup.local` anywhere in its contents.
   - Outputs a final report exactly matching this format to `/home/user/final_report.txt`:
     ```
     Admin: <admin_email>
     Port: <smtp_port>
     Stage: <stage>
     Valid Emails: <count>
     ```
   
   Compile this C program to `/home/user/check_spool` and run it so that `/home/user/final_report.txt` is populated.

Ensure all scripts are executable where appropriate and that you leave `/home/user/final_report.txt` perfectly formatted.