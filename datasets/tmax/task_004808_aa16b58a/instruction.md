You are tasked with debugging a regression in a Rust application that processes container logs. 

A repository is located at `/home/user/log_analyzer`. Recently, the tool started panicking when processing corrupted input payloads, whereas it used to handle them gracefully (returning a structured error and exiting with code 0). 

We know the following:
- The `HEAD` of the `main` branch is broken (panics on corrupted inputs).
- The commit tagged `v1.0` is known to be good.
- There is a test file at `/home/user/corrupted_payload.json` which reliably triggers the panic in the bad versions, but is processed gracefully in the good versions.
- The developer who introduced the regression *also* accidentally hardcoded a secret recovery token into `src/main.rs` in that exact same bad commit. Realizing their mistake, they removed the token in the very next commit.

Your task:
1. Use `git bisect` (and optionally `git bisect run` with a custom script) to efficiently find the exact commit hash that introduced the regression (the first bad commit).
2. Inspect the source code at that specific bad commit to recover the leaked secret token (it will look like `let recovery_token = "SEC-XXXXX";`).
3. Create a file at `/home/user/regression_info.txt` containing exactly two lines:
   COMMIT=<first_bad_commit_hash>
   TOKEN=<recovered_token>

Constraints:
- Do not modify the history of the repository.
- Ensure the Rust application is tested against the `/home/user/corrupted_payload.json` file to determine if a commit is good or bad. Good commits exit with code 0, bad commits crash/panic (non-zero exit).