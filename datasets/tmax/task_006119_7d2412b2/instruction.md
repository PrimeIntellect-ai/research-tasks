You are acting as a backup operator. We need to automate the testing of user data restores without actually modifying live user accounts or overwriting real disk quotas (since you do not have root privileges). 

We have simulated a backup environment in your home directory (`/home/user`). You will find three key items:
1. `/home/user/backup.tar.gz` - A compressed archive containing the files to be restored.
2. `/home/user/backup_manifest.json` - A JSON file containing metadata about the backup, including the original file path, file size, and the UID of the user who owns it.
3. `/home/user/quotas.json` - A JSON file detailing the current storage usage and hard limits for each UID.

Your task is to write and execute a Python script that automates the verification of this restore process. The script must perform the following actions:
1. Extract `/home/user/backup.tar.gz` into a staging directory located at `/home/user/restore_staging/`.
2. Parse `/home/user/backup_manifest.json`. For each file listed in the manifest, check if it was successfully extracted into the staging directory and if its actual byte size matches the `size` specified in the manifest.
3. If the file is missing or the size does not match exactly, mark its restore status as `"size_mismatch"`.
4. If the file is intact and sizes match, evaluate the disk quota for the owning UID based on `/home/user/quotas.json`. 
   - Add the file's size to the UID's `used` storage. 
   - If this new total exceeds the UID's `limit`, mark the restore status as `"quota_exceeded"`. The file's size should *not* be permanently added to the running `used` total if it exceeds the quota.
   - If the new total is within the limit, mark the restore status as `"ok"`, and update the running `used` total for that UID so subsequent files are evaluated correctly.
   - Files should be evaluated in the exact order they appear in `backup_manifest.json`.

Finally, your script must output a JSON file located at `/home/user/restore_report.json`. This file must contain a single JSON object where the keys are the file paths (exactly as they appear in the manifest) and the values are their resulting status (`"ok"`, `"quota_exceeded"`, or `"size_mismatch"`).

Do not change the structure or contents of the input files. All operations should be automated via the Python script or shell commands invoked as part of your solution.