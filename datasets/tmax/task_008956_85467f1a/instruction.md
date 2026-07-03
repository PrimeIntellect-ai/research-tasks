You are a platform engineer responsible for maintaining our CI/CD pipelines. We have a pipeline step defined in a Bash script (`/home/user/ci_build.sh`) that is failing. 

This script is supposed to:
1. Accept a callback webhook URL as its first argument (e.g., `http://ci.local/webhook?job_id=8842&token=sec_991`).
2. Parse the URL to extract the `job_id` parameter.
3. Read `/home/user/job_metadata.json` (which contains configuration for various jobs) to find the expected SHA-256 checksum for this job.
4. Build a Python package located in `/home/user/my_package` into a source distribution (`.tar.gz`).
5. Calculate the SHA-256 checksum of the built package.
6. Generate a JSON report at `/home/user/result.json` with the following structure:
   ```json
   {
     "job_id": "8842",
     "expected_checksum": "<checksum from metadata>",
     "actual_checksum": "<calculated checksum>",
     "match": false
   }
   ```
   (The `match` boolean should be `true` if they match, `false` otherwise).

Currently, the pipeline is completely broken:
- The Python package's `pyproject.toml` has a syntax error or missing mandatory fields, causing `python3 -m build` to fail.
- The Bash script uses a flawed method to extract the `job_id` from the URL.
- The Bash script tries to build JSON using string concatenation which is currently invalid JSON.

Your task:
1. Fix `/home/user/my_package/pyproject.toml` so that the Python package builds successfully. The package name should be `my_package` and version `0.1.0`.
2. Fix the `/home/user/ci_build.sh` script to correctly parse the URL parameter, deserialize the metadata JSON to get the expected checksum, perform the build using `python3 -m build`, compute the actual SHA-256 checksum, and safely serialize the output to `/home/user/result.json`. You may use tools like `jq`, `grep`, `sed`, `awk`, etc.
3. Run the script with the following command to generate the final output:
   `bash /home/user/ci_build.sh 'http://ci.local/webhook?token=abc123&job_id=job_9981&region=us-east'`

Make sure `/home/user/result.json` contains strictly valid JSON and correct values.