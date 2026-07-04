We are building a configuration manager that allows users to upload system configuration backups as `.tar` archives. However, we are concerned about "Tar Slip" attacks where maliciously crafted archives contain absolute paths (e.g., `/etc/passwd`) or directory traversal paths (e.g., `../../root/.ssh/authorized_keys`) to overwrite critical system files during extraction.

Additionally, the lead sysadmin left a voice memo detailing a domain-specific constraint regarding certain file formats that must NEVER be allowed in these uploads, regardless of their paths.

Your task:
1. Locate and transcribe the audio file at `/app/sysadmin_memo.wav` to discover the hidden business rule.
2. Write a Bash script at `/home/user/sanitizer.sh` that takes exactly one argument: the path to a `.tar` archive.
3. The script must analyze the archive's contents (without extracting it).
4. The script must exit with status `0` (success) if the archive is completely safe and valid.
5. The script must exit with status `1` (failure/reject) if the archive contains ANY of the following:
   - Absolute paths (starting with `/`)
   - Directory traversal components anywhere in the path (e.g., `../`, `..`)
   - Files violating the rule dictated in the audio memo.

Ensure your script is executable. You can test your script against any dummy tar files you create. An automated test will run your script against two hidden corpora: one containing exclusively safe archives, and another containing malicious/invalid archives. Your script must correctly classify 100% of both corpora.