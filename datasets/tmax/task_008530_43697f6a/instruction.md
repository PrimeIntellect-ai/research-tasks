You are a DevSecOps engineer responsible for enforcing Security Policy as Code. You need to audit a set of application deployment configurations to identify hardcoded, weak administrator passwords and insecure Content Security Policy (CSP) headers.

You have been provided with the following files in your home directory (`/home/user/`):
1. `deployments.json`: A JSON file containing an array of deployment configurations. Each configuration object has an `app_name`, an `admin_hash` (an MD5 hash of the default administrator password), and a `csp_header` string.
2. `dictionary.txt`: A small list of commonly used weak passwords.
3. `json.hpp`: The nlohmann/json single-header C++ library for JSON parsing.

Your task is to write a C++ program named `/home/user/policy_enforcer.cpp` that performs an automated vulnerability scan and data processing pipeline:
1. Parse `deployments.json` using the provided `json.hpp` library.
2. For each application, verify if the `admin_hash` is derived from any of the passwords in `dictionary.txt`. You will need to compute the MD5 hash of each dictionary word and compare it.
3. Enforce the CSP policy: A `csp_header` is considered non-compliant (insecure) if it contains the exact substrings `unsafe-inline` or `unsafe-eval`.
4. Generate a Comma-Separated Values (CSV) report at `/home/user/audit_report.csv` detailing the audit results.

The output CSV file MUST follow this exact format, including the header row:
```csv
app_name,password_cracked,csp_secure
```
- `password_cracked`: If the hash matches a word in the dictionary, output the plaintext cracked password. If it does not match any word in the dictionary, output `SAFE`.
- `csp_secure`: If the CSP header contains `unsafe-inline` or `unsafe-eval`, output `FAIL`. Otherwise, output `PASS`.

Constraints and Notes:
- Your source file must be located at `/home/user/policy_enforcer.cpp`.
- You must compile and run the program to generate the `/home/user/audit_report.csv` file.
- The standard OpenSSL library (`libssl-dev`) is installed on the system. You can use `<openssl/md5.h>` for cryptographic hashing.
- Ensure your CSV does not contain any extra spaces around commas and has a standard Unix newline (`\n`) at the end of each line.