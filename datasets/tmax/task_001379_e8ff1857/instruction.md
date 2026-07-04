You are a security engineer assisting with credential rotation for our internal SSO portal. During the rotation, we discovered that our login flow is potentially vulnerable to an open redirect attack if the 'redirect_uri' token is manipulated. 

We have a vendored third-party package located at `/app/vendored-sso-auth-1.2.0` that we use to decrypt these tokens. However, the package is currently failing to build because its `Makefile` has a deliberate perturbation: the `LD_FLAGS` variable incorrectly hardcodes an old environment variable path, overriding the system environment and preventing the crypto module from linking correctly. 

Your tasks are:
1. Fix the `Makefile` in `/app/vendored-sso-auth-1.2.0` so that it correctly inherits the system environment and builds properly (run `make` to compile the `sso-decrypt` binary).
2. Write a bash script at `/home/user/redirect_detector.sh` that acts as a classifier. 
   - The script must accept a single argument: the path to a directory containing token files.
   - For each file in the directory, your script should use the fixed `/app/vendored-sso-auth-1.2.0/sso-decrypt` utility to decrypt the token (the utility prints the raw redirect URL to stdout).
   - Your script must analyze the decrypted URL and print exactly `<filename>: CLEAN` if it is a safe, relative path (e.g., `/dashboard`, `/settings`) or exactly `<filename>: EVIL` if it represents an open redirect payload (e.g., absolute URLs pointing to external domains like `http://evil.com`, protocol-relative URLs like `//attacker.com`, or `javascript:` URIs).
   - The output must be printed to `stdout`.

Ensure your script is executable and relies only on standard bash utilities (e.g., `grep`, `awk`, `sed`). Do not use any external APIs or network calls.