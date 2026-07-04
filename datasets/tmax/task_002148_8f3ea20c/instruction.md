You are a DevSecOps engineer responsible for enforcing "Policy as Code" in your organization's deployment pipeline. You need to create a custom security validation tool in C that verifies deployment bundles before they are shipped to production.

A deployment bundle is a directory containing the following:
1. `ca.pem`: The expected Certificate Authority root certificate.
2. `cert.pem`: The endpoint's leaf certificate.
3. `manifest.sha256`: A file containing the expected SHA-256 checksums of the static assets. Format: `<64-char-hex-hash>  <relative-file-path>`
4. `csp.txt`: A text file containing the exact `Content-Security-Policy` HTTP header value for the application.
5. `assets/`: A directory containing various static files (e.g., `index.html`, `app.js`).

Your task is to write a C program located at `/home/user/src/policy_checker.c` and compile it to `/home/user/policy_checker`. The program must take a single command-line argument: the path to a deployment bundle directory.

The program must perform the following three checks:
1. **Certificate Chain Validation**: Use OpenSSL (`libcrypto`/`libssl`) to verify that `cert.pem` is validly signed by `ca.pem`.
2. **File Integrity Verification**: Read `manifest.sha256`. For each file listed, compute its actual SHA-256 hash (using OpenSSL) and ensure it matches the hash in the manifest. (The paths in the manifest are relative to the bundle directory).
3. **CSP Enforcement**: Parse `csp.txt`. Locate the `script-src` directive. The check fails if the `script-src` directive contains the exact string `'unsafe-inline'`. Otherwise, it passes.

Your C program must output the results for the checked bundle to standard output in exactly the following format (including exact spacing and capitalization):
```
BUNDLE: <bundle_directory_path>
CERT: <PASS or FAIL>
INTEGRITY: <PASS or FAIL>
CSP: <PASS or FAIL>
```

Once you have written and compiled your tool (ensure you link against `-lssl -lcrypto`), you must test the four bundles located in `/home/user/bundles/`:
- `/home/user/bundles/dev`
- `/home/user/bundles/staging`
- `/home/user/bundles/prod`
- `/home/user/bundles/dr`

Run your tool on all four directories and redirect the concatenated output to `/home/user/final_report.log`.
The order of the directories in the log file must be: `dev`, `staging`, `prod`, `dr`.