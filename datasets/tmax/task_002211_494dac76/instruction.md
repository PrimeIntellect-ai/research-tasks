You are helping me organize some project submissions from external contributors. We have a directory of incoming archive files and a log file detailing the submissions. Since these are external files, we need to be careful about "Zip Slip" vulnerabilities—where maliciously crafted archives contain paths that attempt to write outside the intended extraction directory (e.g., containing `../` or starting with `/`).

I need you to write a Bash script at `/home/user/organize_projects.sh` that performs the following steps:

1. **Parse the Log:** Read the multi-line log file located at `/home/user/incoming/submissions.log`. Each submission record spans exactly 3 lines, separated by a blank line:
   - Line 1: `ID: <SubmissionID>`
   - Line 2: `Status: <APPROVED|REJECTED>`
   - Line 3: `File: <ArchiveFilename>` (The file will be located in `/home/user/incoming/`)

2. **Process Approved Archives:** For every `APPROVED` submission:
   - Verify the archive's integrity (it could be `.zip` or `.tar.gz`). If it's corrupt, ignore it.
   - Inspect the archive's contents without extracting. If any file path in the archive starts with `/` or contains `../`, flag it as malicious.
   - If it is safe and not corrupt, create a directory at `/home/user/projects/<SubmissionID>/` and extract the archive into it. 

3. **Metadata-based File Search:** After all safe archives are extracted, recursively search through `/home/user/projects/` to find all Python (`.py`) files that have been modified in the last 7 days. Copy all these found Python files into `/home/user/recent_code/` (create this directory if it doesn't exist). Standard stream redirection and piping should be used effectively here.

4. **Summary Report:** Generate a final report at `/home/user/summary.txt` with exactly this format:
   ```
   Safe Extracted: <count_of_safe_archives_extracted>
   Malicious Found: <count_of_malicious_archives_detected>
   Recent Python Files: <count_of_py_files_copied>
   ```

Make sure your script is fully automated and executable. Run your script to complete the organization process.