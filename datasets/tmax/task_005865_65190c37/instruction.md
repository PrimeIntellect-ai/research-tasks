You are managing an artifact repository system. Your job is to write a bash script that curates incoming binary artifacts based on multi-line scan logs, moves approved binaries into the repository, and atomically updates the repository's main manifest file.

Write and execute a bash script at `/home/user/curate.sh` that performs the following actions:

1. **Parse Multi-line Logs:**
   Read the scan log located at `/home/user/logs/scan.log`. 
   The log contains multi-line records separated by a line containing exactly `---`.
   Each record has the following fields (one per line):
   ```
   Artifact: <filename>
   Build-Status: <SUCCESS|FAILED>
   Critical-Vulnerabilities: <integer>
   Warnings: <integer>
   ```
   An artifact is considered **APPROVED** if and only if `Build-Status` is `SUCCESS` AND `Critical-Vulnerabilities` is `0`.

2. **Move Binaries:**
   For every APPROVED artifact, move the corresponding binary file from `/home/user/incoming/` to `/home/user/repo/binaries/`.

3. **Atomically Update the Manifest:**
   The file `/home/user/repo/manifest.txt` contains millions of records, but for this task it has a few thousand. Format: `filename | status | timestamp`.
   For every APPROVED artifact, change its status in the manifest from `PENDING` to `APPROVED`.
   You must do this safely using an atomic write (e.g., write all changes to a temporary file, then `mv` the temporary file over the original `/home/user/repo/manifest.txt`).

4. **Generate Curation Summary:**
   Create a log file at `/home/user/curation_summary.log` containing the exact filenames of the APPROVED artifacts, sorted alphabetically, one per line.

Requirements:
- Only use standard bash built-ins, `awk`, `sed`, `grep`, and coreutils.
- Ensure the script has executable permissions and run it so the final state is achieved.