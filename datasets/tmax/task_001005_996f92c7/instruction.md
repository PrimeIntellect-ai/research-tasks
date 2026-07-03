You are a platform engineer building a lightweight, Bash-based CI/CD pipeline processor for a legacy environment. We need a script that processes a queue of incoming code patches, validates their integrity, enforces rate limits, applies them to a baseline codebase, and tests the result.

Your task is to write a Bash script at `/home/user/ci_system/process_queue.sh` that implements this pipeline. 

The baseline codebase is located at `/home/user/ci_system/src/`. It contains a script `math_utils.sh` which can be run with `./math_utils.sh test` to execute its internal test suite. It exits with `0` on success and non-zero on failure.

The incoming submissions are located in `/home/user/ci_system/submissions/`. For each submission, there are two files:
- `<id>.meta`: A text file containing exactly three lines in the format `KEY=value`:
  - `USER`: The username of the submitter.
  - `TIMESTAMP`: A Unix epoch integer representing the submission time.
  - `CHECKSUM`: The expected SHA-256 hash of the corresponding patch file.
- `<id>.patch`: The unified diff patch file submitted by the user.

Your script must process each submission in **alphabetical order** by the `<id>` prefix and perform the following steps for each:

1. **Rate Limiting**:
   Keep track of the last accepted processing timestamp for each user. A submission is considered `RATE_LIMITED` if the difference between its `TIMESTAMP` and the user's *last non-rate-limited* submission's `TIMESTAMP` is strictly less than 60 seconds. If rate-limited, skip the remaining steps and do not update the user's last tracked timestamp.

2. **Checksum Validation**:
   Calculate the SHA-256 checksum of the `<id>.patch` file. If it does not exactly match the `CHECKSUM` in the meta file, the submission status is `CHECKSUM_FAILED`. Skip the remaining steps (but the user's timestamp *is* updated for rate-limiting purposes since they reached this step).

3. **Patch Processing**:
   Copy the contents of `/home/user/ci_system/src/` to a fresh temporary directory. Attempt to apply `<id>.patch` using the `patch` command (e.g., `patch -p1 < patchfile`). If `patch` fails (returns a non-zero exit code), the status is `PATCH_FAILED`. Skip the remaining steps.

4. **Testing**:
   Run `./math_utils.sh test` in the patched temporary directory. If it exits with a non-zero status, the submission status is `TEST_FAILED`.

5. **Success**:
   If all the above pass, the status is `ACCEPTED`.

For each submission, append exactly one line to `/home/user/ci_system/results.log` in the following format:
`<id> <STATUS>`

Constraints:
- You must write your pipeline processor entirely in Bash.
- Clean up any temporary directories you create.
- The `results.log` file should be created if it does not exist, and should only contain the final results for each `<id>` processed.

Please write and execute the script to generate `/home/user/ci_system/results.log`.