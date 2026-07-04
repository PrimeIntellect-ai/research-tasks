You are a network security engineer investigating a compromised web server. You have intercepted an image of the attacker's terminal (`/app/intercepted_hash.png`) which contains a leaked password hash for the `admin` user. The admin's password is known to be a 4-digit PIN. 

Your objective is to complete a multi-stage security pipeline entirely in Bash:

1. **Hash Recovery & Brute-force:** Extract the text from `/app/intercepted_hash.png` using `tesseract`. Parse the hash, and brute-force the 4-digit PIN. 
2. **CSP Generation Logic:** Write a Bash script at `/home/user/generate_csp.sh` that takes two arguments:
   - `$1`: A path to a target webroot directory (e.g., `/var/www/html`).
   - `$2`: A path to an HTTP response header file.
3. **Permission-based CSP Enforcement:** Your script must dynamically generate a `Content-Security-Policy` header based on the file permissions of the subdirectories inside the webroot (`$1`):
   - By default, set `default-src 'self';`.
   - Iterate over all immediate subdirectories in `$1`.
   - If a subdirectory is world-writable (e.g., `chmod o+w`), append an explicit denial for scripts in that path (e.g., if `/var/www/html/uploads` is world-writable, append `script-src-elem 'none' /uploads;` — assume relative to webroot).
   - If a subdirectory has the sticky bit set (e.g., `chmod +t`), append `object-src 'none';`.
4. **Header Injection:** Your script must output the exact contents of the HTTP response header file (`$2`), but with the newly generated `Content-Security-Policy` header injected immediately before the blank line separating headers from the body. Additionally, inject a custom header `X-Admin-Pin: <cracked_pin>` using the 4-digit PIN you cracked in step 1.

The script must handle standard HTTP header formatting (CRLF line endings) and must be deterministic. Do not use Python; rely strictly on Bash, standard coreutils, `awk`, `sed`, `tesseract`, and basic brute-force tools (like `john` or standard hashing commands). Ensure `/home/user/generate_csp.sh` is executable.