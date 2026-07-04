You are an engineer tasked with diagnosing and fixing a deployment issue for a mailing list service. The service failed to start, and its log output has been saved to `/home/user/service_logs.txt`. 

Your task is to:
1. Use text processing tools to inspect `/home/user/service_logs.txt` and identify the missing configuration values (Admin Email and SMTP Port) that caused the fatal error.
2. The service provides an interactive configuration script at `/home/user/mail_config_wizard.sh` to fix these settings.
3. Write an Expect script at `/home/user/fix_mail.exp` that automatically runs `/home/user/mail_config_wizard.sh` and provides the exact values extracted from the log file.
4. The interactive wizard will prompt exactly for:
   `Enter Admin Email: `
   `Enter SMTP Port: `
5. Execute your Expect script so that the wizard successfully completes and generates the repaired configuration file at `/home/user/mail_config.conf`.

Requirements:
- Your Expect script must be saved at `/home/user/fix_mail.exp`.
- The final configuration file `/home/user/mail_config.conf` must be successfully generated with the correct values from the log.
- Do not hardcode guesses; derive the values specifically mentioned in the "FATAL ERROR" details within the log file.