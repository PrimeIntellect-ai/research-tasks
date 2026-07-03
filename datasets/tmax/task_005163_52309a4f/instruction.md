You are a security engineer assigned to rotate credentials and harden the SSH infrastructure for a critical server. We have discovered that users have been injecting malicious commands into their `authorized_keys` files, and some are still using cryptographically weak keys. 

Your tasks are:

1. **Fix the Auditing Tool**: We use a vendored version of `ssh-audit` located at `/app/ssh-audit-3.1.0/`. However, it currently crashes when executed due to a deliberate perturbation (a broken import or typo in the main script). Identify and fix the script so it can run successfully.

2. **Develop an Authorized Keys Filter**: Write a Bash script at `/home/user/validate_auth_keys.sh`. This script will be used as a pre-commit hook to sanitize `authorized_keys` files.
   - It must read lines from standard input.
   - It must output (to standard output) ONLY the lines that are cryptographically secure and free of injection vulnerabilities.
   - **Criteria for Rejection**:
     - Reject weak key types: `ssh-dss` or `ssh-rsa`.
     - Reject lines containing potential command or environment injection vulnerabilities in the options field (e.g., shell metacharacters like `|`, `&`, `$`, `` ` ``, `;`, or the `environment=` option).
   - **Criteria for Acceptance**:
     - Accept strong key types: `ssh-ed25519` or `ecdsa-sha2-nistp256`.
     - Allow safe options like `restrict` or absolute path command restrictions (e.g., `command="/usr/bin/rsync"` without shell metacharacters).
   - We have provided a set of test cases. Your script must preserve 100% of the lines in the clean corpus (`/app/corpora/clean/`) and reject 100% of the lines in the evil corpus (`/app/corpora/evil/`).

3. **Key Rotation**: Generate a new, secure `ed25519` SSH keypair for the admin user. Save the private key to `/home/user/admin_key` with an empty passphrase. Ensure the permissions on the private key are properly hardened.

Your final solution will be evaluated automatically by running your filter against our hidden evaluation corpora and verifying the functionality of the `ssh-audit` tool and the new keys.