You are a backup administrator maintaining an automated archiving system. An external service has generated an incremental backup manifest at `/home/user/incremental_manifest.txt`. However, this service is untrusted, and the manifest may contain malicious file paths designed to overwrite system files during archive extraction (similar to a "zip slip" attack).

Your task is to parse this manifest and create a sanitized version. 

Perform the following steps using bash commands:
1. Read the list of files from `/home/user/incremental_manifest.txt`.
2. Filter out any malicious or unsafe paths using standard stream redirection and piping. A path is considered UNSAFE and must be removed if it meets any of the following criteria:
   - It is an absolute path (starts with `/`).
   - It contains a parent directory traversal component (i.e., it contains `../`, `/..`, or is exactly `..`).
3. To prevent race conditions where the backup runner might read a partially written file, you must write the sanitized list using an atomic write pattern. First, redirect your filtered output into a temporary file named `/home/user/safe_manifest.tmp`.
4. Finally, atomically rename the temporary file to the final destination: `/home/user/safe_manifest.txt`.

Ensure the final `/home/user/safe_manifest.txt` contains only the safe, relative paths, preserving their original order.