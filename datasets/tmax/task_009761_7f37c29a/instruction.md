As a backup administrator, you are auditing our archive extraction systems for "Zip Slip" (path traversal) vulnerabilities. To test our extraction tools, you need to deliberately construct a malicious tar archive that mimics a backup payload containing path traversal attempts and symlinks.

Your task is to:
1. Write a Python script at `/home/user/make_test_tar.py` that creates an uncompressed tar archive named `/home/user/vuln_backup.tar`.
2. The archive MUST contain exactly these three entries:
   - A regular file named `config.txt` containing the exact text `SAFE_MODE=1`.
   - A symbolic link named `config_link.txt` that points to `config.txt` (this tests how our system handles symlinks inside archives).
   - A file with a malicious path traversal name explicitly set as `../pwned.txt`. The contents of this malicious file must be `YOU_HAVE_BEEN_COMPROMISED`.
3. Execute your Python script to generate the `/home/user/vuln_backup.tar` archive.
4. Using bash shell commands, list the contents of the newly created tar file using `tar -tvf` and redirect standard output to a log file located at `/home/user/archive_list.log`.

Do not extract the archive yourself. Just generate the payload archive and the log file. Ensure you set the correct file types (e.g., symlink vs regular file) and file names (specifically the traversal path) in the tarball metadata.