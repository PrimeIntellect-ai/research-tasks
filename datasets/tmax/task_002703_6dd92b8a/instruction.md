As a site administrator, I need to modernize our user account management by moving it to a Git-based workflow. I want to validate user profiles when they are pushed to a central repository and extract a daily report of registered emails using classic text-processing pipelines. 

Please perform the following setup:

1. **Create the Bare Repository**: 
   Initialize a bare Git repository at `/home/user/auth_server.git`.

2. **Pre-receive Hook & Python Validator**:
   There is a file at `/home/user/banned_users.txt` containing one forbidden username per line.
   Create a Python script at `/home/user/validate_user.py` and hook it up as the `pre-receive` hook for `/home/user/auth_server.git`. 
   
   The hook must read the standard Git `pre-receive` input from `stdin` (`<oldrev> <newrev> <refname>`). For every commit being pushed, it must inspect the files that were added or modified.
   If any modified/added file is in the `accounts/` directory, it must enforce the following rules:
   - The file path must end with `.json` (e.g., `accounts/johndoe.json`). The filename without `.json` is considered the username.
   - The username must NOT exist in `/home/user/banned_users.txt` (case-insensitive exact match).
   - The file must contain a valid JSON payload.
   - The JSON payload must contain the key `"email"`.
   
   If any of these conditions are violated, the push must be rejected (exit code > 0). Otherwise, it should be accepted.

3. **Text Processing Pipeline**:
   Write a bash script at `/home/user/extract_emails.sh`. When executed, this script should:
   - Clone `/home/user/auth_server.git` to a temporary directory.
   - Process all `.json` files inside the `accounts/` directory using basic UNIX text processing tools (`grep`, `awk`, `sed`, etc.). **Do not use `python` or `jq`** in this bash script. 
   - Extract the username (from the filename) and the email (from the file contents). Note: you can assume the email line in the JSON will exactly match the format: `"email": "some@address.com"` (ignoring leading whitespace).
   - Write the output to `/home/user/active_emails.csv` in the exact format: `username,email`.
   - Clean up the temporary directory before exiting.

4. **Scheduled Task**:
   Write a valid crontab entry that would run the `/home/user/extract_emails.sh` script daily at exactly 2:00 AM. Save this single line of cron configuration to `/home/user/my_cron.txt`.

Ensure all scripts are executable. Do not start any persistent daemons. You can test your setup by creating a local clone of the repository, adding files to the `accounts/` directory, and pushing them to `auth_server.git`.