You are a site administrator for a company, but you do not have root access on the primary server. You need to build a user management automation script to handle onboarding and auditing using a simulated local directory structure.

Your objective is to write a Bash script `/home/user/onboard.sh` that processes a CSV file of new hires, creates simulated user accounts, provisions simulated mailing list entries, and audits an access log for locked accounts. 

**Phase 1: Automated Onboarding**
Write a script `/home/user/onboard.sh` that takes a CSV file path as its first argument.
The CSV file (e.g., `/home/user/new_hires.csv`) has a header row and follows this format:
`FirstName,LastName,Department,Email`

For each record in the CSV (skipping the header), your script must:
1. **Generate a Username:** Take the first letter of the First Name, concatenate it with the Last Name, convert it to lowercase, and truncate it to a maximum of 8 characters. If the resulting username already exists in `/home/user/site_data/passwd`, append the digit `1` to the end of the truncated base string. If that also exists, append `2`, and so on.
2. **Create Passwd Entry:** Append a line to `/home/user/site_data/passwd` using the standard format: `username:x:UID:GID:FirstName LastName:/home/user/site_data/home/username:/bin/bash`. 
   - Assign the next available UID starting from `1000` (if the file is empty, use `1000`; otherwise, max(UID) + 1).
   - The GID depends on the Department: `Engineering` = 2000, `Sales` = 2001, `HR` = 2002.
3. **Create Home Directory:** Create the user's home directory at `/home/user/site_data/home/<username>`.
4. **Update Mailing Lists:** Append the user's raw email address to the appropriate department mailing list file located at `/home/user/site_data/lists/<Department>.list` (e.g., `Engineering.list`). Create the file if it does not exist.
5. **Generate Welcome Email:** Create a file at `/home/user/site_data/mail_spool/<username>.txt` with exactly these two lines:
   ```
   To: <Email>
   Subject: Welcome to <Department>, <FirstName>!
   ```

**Phase 2: Log Auditing**
After onboarding the CSV, your script must parse the log file located at `/home/user/access.log`. 
1. Use text processing pipelines (e.g., awk, sed, grep) to find all lines containing the string `STATUS=LOCKED`.
2. Extract the username from those lines (the log format is: `YYYY-MM-DD HH:MM:SS [username] action STATUS=...`).
3. For each locked out username, find their email address from the newly populated CSV data (or cross-reference with the mailing lists) and append their email to `/home/user/site_data/locked_emails.txt`.
4. Remove the locked-out users' emails from all files in `/home/user/site_data/lists/`.

**Execution:**
You must write the script `/home/user/onboard.sh`, make it executable, and run it against `/home/user/new_hires.csv`. 

Before you start, the `/home/user/site_data/` directory tree, the initial `access.log`, and `new_hires.csv` will already be present.