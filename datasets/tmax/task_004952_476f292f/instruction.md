You are an infrastructure engineer automating the provisioning of a secure mail filtering and forwarding gateway.

Your task consists of three parts:

1. **Fix a Vendored Package**
You have been provided with a vendored simple SMTP stub server located at `/app/smtpd-stub-0.0.1`. The startup script `/app/smtpd-stub-0.0.1/run.sh` has a bug: it hardcodes the listening port to `0` instead of reading it from the `SMTP_PORT` environment variable. 
Modify `/app/smtpd-stub-0.0.1/run.sh` so that it passes the `SMTP_PORT` environment variable to the `server.py` script. If `SMTP_PORT` is not set or empty, it should default to `2525`.

2. **Develop an Email Classifier**
To protect the internal network, you must create a script that detects malformed or malicious incoming emails. 
Create an executable script at `/home/user/classify_email` (you can write this in bash, python, or any language of your choice) that takes a single argument: the path to an `.eml` file.
The script must analyze the file and determine if it is "clean" or "evil".
An email is considered "evil" if it meets *either* of the following conditions:
- It contains more than one line starting with `Subject:` (case-insensitive, e.g., `subject:`, `SUBJECT:`).
- It contains the exact string `X-Admin-Bypass: 1` anywhere in the file.
If the email is clean, your script must exit with status code `0`. If the email is evil, it must exit with status code `1`.
*Note: A corpus of test emails is available at `/app/emails/clean/` and `/app/emails/evil/` for you to test your script.*

3. **Create a Setup Profile**
Create a shell profile script at `/home/user/mail_profile.sh` that sets up the environment for the mailer. This script must:
- Export the environment variable `SMTP_PORT` with the value `8025`.
- Export the environment variable `MAIL_CLASSIFIER` with the value `/home/user/classify_email`.
- Define a bash function named `start_tunnel` that, when called, executes exactly the following command to set up an SSH port forward to the legacy mail server:
  `ssh -f -N -L 8025:localhost:25 mailadmin@mail.local -i /home/user/.ssh/mail_rsa`

Ensure your classifier is executable and works correctly before concluding the task.