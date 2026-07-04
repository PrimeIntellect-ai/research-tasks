You are a DevSecOps engineer enforcing policy-as-code. You need to create a custom deployment validation tool in C that acts as a gatekeeper for configuration deployments.

Your objective is to write, compile, and execute a C program called `deploy_validator` that checks deployment tokens, verifies payload integrity, and scans for malicious patterns. 

Create the workspace directory `/home/user/deploy_check`. All work should be done here.

1. Write a C program named `deploy_validator.c` in `/home/user/deploy_check/`.
2. The program must take exactly three command-line arguments:
   `./deploy_validator <token> <payload_file_path> <expected_sha256_hex>`
3. The program relies on the environment variable `DEPLOY_SECRET`. If this is not set, the program should print `DENY: Internal error` and exit with code 1.

The program must perform the following checks in order:

**Check 1: Token Validation**
The token must strictly follow the format: `DEP-<username>-<signature>`
- `username` is an alphanumeric string.
- `signature` is the SHA-256 hash (in lowercase hex) of the string concatenated as: `<username><DEPLOY_SECRET>`
If the token does not match this format or the signature is incorrect, print `DENY: Invalid token` and exit with code 1.

**Check 2: Checksum Verification**
The program must compute the SHA-256 hash of the file located at `<payload_file_path>`.
If the computed lowercase hex hash does not exactly match the `<expected_sha256_hex>` argument, print `DENY: Hash mismatch` and exit with code 1.

**Check 3: Intrusion Detection Pattern Matching**
The program must scan the contents of the payload file for any of the following exact strings:
- `system(`
- `/bin/sh`
- `curl | bash`
- `eval(`
If any of these substrings are found anywhere in the file, print `DENY: Malicious payload` and exit with code 1.

**Success:**
If all checks pass, print exactly `ALLOW` and exit with code 0.

**Testing:**
Compile your program to `/home/user/deploy_check/deploy_validator`. You may use OpenSSL (`-lcrypto`) for cryptographic functions.

After compiling, create a script `/home/user/deploy_check/run_tests.sh` that sets `export DEPLOY_SECRET="AlphaBravo123"` and tests the program with the following 4 scenarios. For each scenario, append the output of the C program to `/home/user/deploy_check/validation_results.log`. 
Create the necessary payload files to trigger these conditions:
1. An invalid token.
2. A valid token, but the expected file hash does not match the actual file hash (use a benign file).
3. A valid token, a matching hash, but the file contains the string `curl | bash`.
4. A valid token, a matching hash, and a completely benign file (e.g., just containing the text "config_version=1.0").

Run your script to generate the `/home/user/deploy_check/validation_results.log` file.