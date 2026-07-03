You are an artifact manager AI responsible for curating binary repositories. We have a problem with "Zip Slip" vulnerabilities where malicious archives contain paths (like `../../etc/passwd`) designed to extract files outside the designated target directory.

Your task is to write a Python utility at `/home/user/sanitize.py` that processes archive manifests, filters out dangerous paths, and safely logs the results. 

Requirements for `/home/user/sanitize.py`:
1. **Invocation:** The script must take exactly two arguments: a target base directory and an input manifest file.
   `python3 /home/user/sanitize.py <target_base_dir> <manifest_file>`
2. **Policy Extraction:** There is an image artifact located at `/app/policy.png`. Read this image (using OCR, e.g., `tesseract`) to extract the "ACTIVE REPO ID" (it will be a string like `REPO-XXXX`).
3. **Path Sanitization:** The `<manifest_file>` contains one archive file path per line. For each line:
   - Compute the absolute path as if the file were extracted inside the `<target_base_dir>`. 
   - Normalize the path (resolve all `.` and `..`).
   - Determine if the resolved absolute path strictly falls inside the absolute path of `<target_base_dir>`.
   - If it falls outside (or exactly on) the base directory, it is a Zip Slip attack and must be discarded.
4. **Output:** For every *safe* path, your script must print to standard output (stdout):
   `[<ACTIVE_REPO_ID>] <resolved_absolute_path>`
   (e.g., `[REPO-1234] /home/user/target/valid_file.bin`)
5. **Concurrent Logging:** In addition to stdout, your script must append the exact same output lines to `/tmp/artifact_db.log`. Because multiple extractors run concurrently, you **must** use `fcntl.flock` to acquire an exclusive lock on `/tmp/artifact_db.log` before writing, and release it afterward.

Write the complete `/home/user/sanitize.py` script. Do not execute it yourself; an automated fuzzing suite will invoke your script with various dangerous paths and check its stdout against an oracle implementation.