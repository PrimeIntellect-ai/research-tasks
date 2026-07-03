You are acting as a compliance analyst tasked with generating an audit trail for a legacy authentication gateway. We recently discovered that an older version of our identity provider was generating vulnerable access tokens, and we need to quantify the blast radius.

Your task is to analyze a dataset of JWT tokens and cross-reference them with our SSH logs to identify vulnerable sessions.

Here is what you have:
1. `/app/tokens.txt`: A file containing 5,000 JWT tokens (one per line).
2. `/app/ssh_logs.txt`: A log file containing SSH connection attempts, including the public key fingerprints used for authentication.
3. `/app/architecture.png`: An architecture diagram of the legacy system. You must read this image to find the hardcoded HMAC signing secret used by the legacy gateway.

You need to write a script (in bash, python, or your language of choice) to process these tokens and generate an audit report.

Requirements for the audit report:
- Create a CSV file at `/home/user/vulnerable_audit.csv`.
- The CSV must have the following headers exactly: `token_id,vulnerability_type,associated_ssh_fingerprint`
- `token_id`: The `jti` (JWT ID) claim from the token payload.
- `vulnerability_type`:
  - If the token's header specifies `"alg": "none"`, mark it as `alg_none`.
  - If the token is signed with a weak secret (the one found in `/app/architecture.png`), mark it as `weak_signature`. (You must validate the HMAC-SHA256 signature to determine this).
  - If the token is validly signed but has an `exp` claim in the past (assume current Unix epoch time is `1710000000` for this audit), mark it as `expired`.
  - If the token has none of these issues, do not include it in the CSV.
- `associated_ssh_fingerprint`: Cross-reference the `sub` (subject/username) claim in the JWT with `/app/ssh_logs.txt` to find the most recent SSH key fingerprint used by that user. If no SSH log exists for the user, leave it empty.

Your final output will be evaluated by an automated scoring system that calculates the F1-score of your vulnerability classifications against our internal ground truth. You must achieve an F1-score of `>= 0.95`.