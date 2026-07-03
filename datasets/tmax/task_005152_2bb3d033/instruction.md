You are acting as a compliance analyst tasked with generating secure audit trails. You have been given a raw application log file that contains sensitive credit card information, and you need to redact it securely before the log can be stored. Instead of destroying the sensitive data, you must encrypt it so authorized personnel can recover it later. 

Your task is to write a Python script and perform a security scan on it.

Perform the following steps:

1. Write a Python script at `/home/user/redact_audit.py`.
2. The script must read the log file `/home/user/raw_audit.log`. 
3. Identify all 16-digit credit card numbers in the log. You can assume they appear as exactly 16 consecutive digits bounded by non-digit characters (e.g., regex `\b\d{16}\b`).
4. Read a Fernet symmetric key from `/home/user/fernet.key`.
5. For each 16-digit number found, encrypt the string representation of the number using the `cryptography.fernet.Fernet` class with the provided key.
6. Replace the original 16-digit number in the log text with the format: `ENC(<encrypted_token>)` where `<encrypted_token>` is the decoded utf-8 string of the Fernet encryption output.
7. Write the modified log contents to `/home/user/safe_audit.log`.
8. Once the script is written and you have successfully generated `/home/user/safe_audit.log`, run an automated vulnerability scan on your script using `bandit`. Output the results in JSON format to `/home/user/bandit_report.json`.

Ensure your Python script runs correctly and processes the file without altering any other text in the logs.