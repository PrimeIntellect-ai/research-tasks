You are a DevSecOps engineer enforcing policy as code for a legacy microservice. You have been given an application package located at `/home/user/app_package/`. You need to audit its authentication token generation and its Content Security Policy (CSP) configurations.

Your tasks are as follows:

1. **Reverse Engineering & Token Forging:**
   Inside the package, there is a compiled Python bytecode file `/home/user/app_package/legacy_auth.pyc`. It contains a legacy function `generate_token(user_id)` that was used to create access tokens.
   - Analyze (disassemble or reverse engineer) the `legacy_auth.pyc` file to understand the underlying token generation algorithm and extract its static encryption key.
   - Write a Python script at `/home/user/forge_token.py` that replicates this algorithm.
   - Use your script to generate a valid token for the user ID `admin_root`.
   - Save the exact string of the generated token for `admin_root` into a file located at `/home/user/admin_token.txt`.

2. **Content Security Policy Enforcement:**
   Also in the package is `/home/user/app_package/csp_rules.json`, containing a JSON list of application configurations and their associated CSP strings.
   - Enforce our new security policy by filtering out any configuration where the `policy` string contains the substrings `'unsafe-inline'` or `'unsafe-eval'`.
   - Output the compliant configurations (keeping the exact same JSON schema: a list of objects with `id` and `policy` keys) to a new file at `/home/user/safe_csp.json`. The output must be valid JSON.

Ensure both `/home/user/admin_token.txt` and `/home/user/safe_csp.json` are created with the correct data.