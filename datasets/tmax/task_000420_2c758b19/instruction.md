You are a support engineer tasked with collecting diagnostics and identifying the root cause of a recent data pipeline failure. Our edge devices send diagnostic payloads, but a recent backend update introduced a subtle bug related to timezone offset calculations and data query transformations.

You have two main objectives:

**Objective 1: Replicate the Legacy Validator**
We have a legacy proprietary binary located at `/app/diag_oracle`. It is a stripped binary that validates incoming diagnostic payloads (JSON files). It exits with code `0` if a payload is perfectly valid, and `1` if it is corrupted or maliciously crafted ("evil").
Because this binary is an unmaintained black-box, you must write a Go CLI program at `/home/user/diag_filter.go` that perfectly replicates its classification logic. 
- Your Go program must compile to `/home/user/diag_filter`.
- It must take a single command-line argument: the path to a JSON payload file.
- It must exit with code `0` if the payload is valid, and code `1` if it is invalid.
- You can use `/app/diag_oracle` as a black-box oracle to figure out what constitutes a valid vs. invalid payload by feeding it test files. (Hint: look at the relationship between the timestamp, timezone offset, and the data checksum).

**Objective 2: Git Bisection**
Our new backend service repository is located at `/home/user/diag_service`. It contains a test suite (`go test ./...`) that validates data transformation diffs and query results. Recently, a subtle bug was introduced that causes timezone boundaries to be calculated incorrectly, breaking the query results.
- You must use `git bisect` to find the exact commit hash that introduced the regression. 
- The commit `HEAD` is currently broken, but the tag `v1.0.0` is known to be good.

**Final Output Requirement**
Create a diagnostic report at `/home/user/report.txt` with exactly two lines:
Line 1: The full Git commit hash of the bad commit in `/home/user/diag_service`.
Line 2: The path to your compiled Go filter (`/home/user/diag_filter`).

Ensure your Go filter is robust, as it will be automatically tested against a hidden corpus of valid and evil payloads to verify your implementation.