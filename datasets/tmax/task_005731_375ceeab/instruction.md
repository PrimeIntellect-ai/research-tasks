You are acting as a configuration manager for a legacy application. The system tracks deployments using a multi-line text log file. We need to identify exactly which configuration files have changed since the last successful deployment.

Your task is to write and execute a Bash script at `/home/user/tracker.sh` that does the following:

1. **Parse the Deployment Log**: Read `/home/user/deploy.log`. This file contains multi-line records of past deployments. A record looks like this:
   ```
   [DEPLOY_START]
   ID: 1042
   Status: SUCCESS
   Files:
    - /home/user/app_config/db.yaml (sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855)
    - /home/user/app_config/api.conf (sha256: ...)
   [DEPLOY_END]
   ```
   You must identify the *most recent* (last in the file) deployment record that has `Status: SUCCESS`. Extract the list of tracked files and their expected SHA-256 hashes from this specific record.

2. **Scan the Configuration Directory**: Find all `.yaml` and `.conf` files currently located in the directory `/home/user/app_config/`. Do not process files with other extensions.

3. **Compute and Compare Checksums**: Compute the current SHA-256 hash of the found files and compare them against the state from the last successful deployment.

4. **Generate a Report**: Create a report at `/home/user/pending_changes.txt` containing the drift analysis. Each line must be formatted exactly as follows depending on the file's state, and the file must be sorted alphabetically by the file path:
   - For a file present in the directory but not in the last successful deployment: `NEW: <filepath> (sha256: <current_hash>)`
   - For a file present in the directory AND in the deployment, but with a different hash: `MODIFIED: <filepath> (sha256: <current_hash>)`
   - For a file present in the deployment but missing from the directory: `DELETED: <filepath>`

Do not include files that are unmodified. Ensure your script handles paths correctly and produces exactly the requested format. Run your script so that `/home/user/pending_changes.txt` is generated.