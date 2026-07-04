You are managing a user-hosted PaaS environment. One of the users, Alice, is experiencing a 502 Bad Gateway on her application, and her deployments via Git are failing.

You need to write an idempotent Python script at `/home/user/fix_site.py` that performs the following system administration tasks to resolve her issues:

1. **Fix Nginx Configuration:**
   Alice's local Nginx configuration file is located at `/home/user/nginx/conf/alice.conf`. Currently, it has a misconfigured `proxy_pass` upstream socket path (e.g., pointing to `/tmp/wrong.sock`). 
   Your Python script must read this file and replace the wrong socket path with the correct one: `http://unix:/home/user/apps/alice/app.sock`. Make sure the script is idempotent (if it's already correct, it makes no changes).

2. **Git Hook & Storage Monitoring:**
   Alice deploys her app by pushing to `/home/user/git/alice.git` (a bare repository). We need to enforce a soft storage quota.
   Your script must generate a Python `pre-receive` hook at `/home/user/git/alice.git/hooks/pre-receive`. 
   The hook must:
   - Calculate the total disk space used by the directory `/home/user/apps/alice` (summing file sizes).
   - If the total size is strictly greater than 50,000,000 bytes, print exactly "Error: Quota exceeded" to standard output and exit with status code 1.
   - Otherwise, exit with status code 0.
   Ensure the hook is executable.

3. **Interactive Admin Tool:**
   Alice's account is locked. There is a legacy interactive Python CLI tool at `/home/user/scripts/admin_tool.py`.
   Your script (`/home/user/fix_site.py`) must use a tool like `pexpect` (or call a bash `expect` script) to run `/home/user/scripts/admin_tool.py unlock alice`.
   The interactive flow is:
   - Prompt: `Admin Password: ` -> Send `supersecret99`
   - Prompt: `Confirm unlock for alice? (y/n): ` -> Send `y`
   If successful, the tool will automatically create a verification file.

Requirements:
- Your primary automation must be inside `/home/user/fix_site.py`.
- You can run the script yourself to test it.
- Do not assume you have `sudo` access.
- When you are done, execute your script so the system reaches the desired state. 
- Leave the `/home/user/fix_site.py` file on disk for final verification.