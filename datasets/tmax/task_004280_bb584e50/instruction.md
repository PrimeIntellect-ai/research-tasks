You are a Linux systems engineer responsible for hardening our reverse proxy and load balancer deployments. We manage our Nginx configurations using a local bare Git repository located at `/home/user/proxy-repo.git`. 

To prevent developers from accidentally deploying insecure TLS configurations, you need to implement a Git server hook that validates incoming configuration files.

Please complete the following tasks:

1. **Create a validation script in Python:**
   Write a Python script at `/home/user/check_tls.py`. This script must:
   - Read text from standard input (`sys.stdin`).
   - Search the text for the exact substrings `TLSv1` or `TLSv1.1`. (Note: `TLSv1.2` and `TLSv1.3` are safe, but if the string is exactly `TLSv1` or `TLSv1.1` surrounded by spaces/punctuation, or just the raw substring `TLSv1.1` or `TLSv1 `—actually, to be precise, just check if the exact substring `TLSv1.1` is in the text, OR if the text contains `TLSv1` NOT immediately followed by `.2` or `.3`). 
   - For simplicity, if the input contains `TLSv1.1`, or contains `TLSv1` followed by a space or semicolon (e.g., `TLSv1;` or `TLSv1 `), it should be flagged. 
   - If flagged, print exactly `WEAK TLS DETECTED` to standard output and exit with status code `1`.
   - If not flagged, exit with status code `0`.
   - Ensure the script is executable.

2. **Configure the Git Hook:**
   Create a `pre-receive` hook at `/home/user/proxy-repo.git/hooks/pre-receive`. This bash script must:
   - Read the `<old-value> <new-value> <ref-name>` from standard input (as standard for pre-receive hooks).
   - Use `git diff-tree` and text processing tools (e.g., `awk`, `grep`) to identify any files ending in `.conf` that were added or modified in the push.
   - For each modified/added `.conf` file, use `git show` or `git cat-file` to extract the incoming contents of the file and pipe it into `/home/user/check_tls.py`.
   - If `/home/user/check_tls.py` exits with code `1` for *any* file, the `pre-receive` hook must immediately exit with code `1` to reject the push.
   - If all `.conf` files pass (or if no `.conf` files were changed), the hook must exit with code `0` to allow the push.
   - Ensure the hook is executable.

Do not use root/sudo, as you are operating within the `/home/user` directory.