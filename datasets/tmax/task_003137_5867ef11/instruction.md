You are an artifact manager responsible for curating incoming binary repositories. We receive various `.zip` and `.tar.gz` archives in our incoming queue. However, we have been warned that some submissions might be corrupted or malicious, specifically containing "Zip Slip" or path traversal payloads (files attempting to extract outside the intended extraction directory using `../`).

Your task is to write and execute a Python script at `/home/user/curate_artifacts.py` that securely processes all archives found in `/home/user/incoming_artifacts/`.

For every archive in the incoming directory, the script must:
1. **Verify Integrity & Security:** Check if the archive is a valid, uncorrupted `.zip` or `.tar.gz` file. Then, inspect the archive's file list to ensure no file path resolves outside the target extraction directory (e.g., contains absolute paths or `../` traversals).
2. **Handle Invalid/Malicious Archives:** If an archive is corrupted or contains a path traversal attempt, it must NOT be extracted. Instead, atomically move the archive to `/home/user/quarantine/` and append a line to `/home/user/artifact_audit.log` exactly in this format:
   `[REJECTED] <filename>: <Reason>`
   (Where `<Reason>` is either `Corrupted` or `Path Traversal`).
3. **Safely Extract Valid Archives:** If the archive is safe, extract its contents into a directory at `/home/user/curated_artifacts/<archive_name_without_extension>/`. To ensure no partial extractions are visible to consumers, you must use **atomic writes**: extract the contents into a temporary directory first, and only rename it to the final destination directory once extraction is 100% complete. After extraction, delete the original archive from the incoming directory.

**Directory Structure (to be created if they don't exist):**
- `/home/user/incoming_artifacts/` (already contains the files)
- `/home/user/curated_artifacts/`
- `/home/user/quarantine/`

Write the Python script, run it, and ensure all incoming artifacts are correctly categorized, extracted, or quarantined.