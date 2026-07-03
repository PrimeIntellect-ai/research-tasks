You are a container specialist managing a microservices environment. We have a scheduled job that generates mailing list activity reports via a Go application. However, due to environment variable misconfigurations and a bug in the code, the job is writing reports to the wrong directory, using the wrong timezone/locale, and ignoring our SMTP port configuration.

Your objective is to fix the setup, code, and configurations so the service behaves correctly.

Here are the requirements:

1. **Fix the Environment Variables in the Runner:**
   There is a shell script at `/home/user/run_job.sh`. It is supposed to execute the Go program, but it fails to properly export the required environment variables. Fix the script so it exports the following variables before executing the Go code:
   - `REPORTS_DIR=/home/user/reports`
   - `TZ=America/Los_Angeles`
   - `LC_ALL=en_US.UTF-8`
   - `SMTP_PORT=2525`

2. **Fix the Go Application:**
   The Go source code is located at `/home/user/app/mailer.go`. 
   It has a bug: it is supposed to read the `REPORTS_DIR` environment variable to determine where to create the `report.txt` file. However, due to a variable shadowing issue, it always creates the directory and writes the file to the fallback location (`/tmp/default_reports`).
   Fix the bug in `/home/user/app/mailer.go` so it properly uses the `REPORTS_DIR` environment variable to define the output directory. It must create the directory if it does not exist.

3. **Fix the Configuration File:**
   The mailing list microservice relies on a configuration file located at `/home/user/config/smtp.json`. Ensure the file contains exactly this JSON structure (and create it/the directory if missing):
   ```json
   {
       "mailing_list": "active",
       "protocol": "smtp"
   }
   ```

4. **Execution:**
   Once everything is fixed, run the `/home/user/run_job.sh` script.

If done correctly, executing `/home/user/run_job.sh` will compile and run the Go application, generating the file `/home/user/reports/report.txt`. The contents of `report.txt` are automatically formatted by the Go script to include the local time (in the `America/Los_Angeles` timezone), the locale, and the SMTP port. Do not modify the formatting logic in the Go script.