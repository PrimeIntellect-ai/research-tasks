As a backup administrator for a secure data facility, you are tasked with recovering and archiving a highly sensitive batch of audio logs and metadata manifests. The previous automated pipeline was compromised, so you must rebuild the process using Rust and standard Linux tools.

Your workflow consists of four critical stages:

1. **Audio Extraction:**
There is a voice memo located at `/app/audio/directive.wav`. Transcribe the spoken audio. The speaker will state a specific authorization prefix (e.g., "The authorization code is..."). Save this exact prefix string (lowercased, spaces replaced with underscores) to `/home/user/auth_prefix.txt`.

2. **Adversarial Log Filtration (Rust):**
We have intercepted backup metadata logs, but some are poisoned with path traversal attacks and integer overflows. 
Write a Rust command-line tool at `/home/user/log_filter/` that acts as a sanitizer.
It must read a JSON log file and print ONLY the valid JSON objects to standard output (one per line). 
- A valid log entry has a `"file_path"` that does NOT contain `../` or absolute paths targeting outside `/backup/` (e.g., `/etc/passwd`).
- A valid log entry has a `"size_bytes"` that is a non-negative integer.
- The program should be invocable via `cargo run --release -- <path_to_log>`.

3. **Bulk File Renaming:**
In `/app/raw_backups/`, there are hundreds of data files. Bulk rename all files in this directory by prepending the authorization prefix you extracted in step 1, followed by a hyphen. (e.g., `data_1.bin` -> `auth_prefix-data_1.bin`). 

4. **Differential Backup:**
Create a tar-based differential backup of `/app/raw_backups/` (after renaming) and store the archive at `/home/user/secure_archive/diff_backup.tar`. Use `/home/user/secure_archive/backup.snar` as the snapshot file for the `--listed-incremental` flag. Base this differential backup off the existing full backup snapshot located at `/app/baseline/baseline.snar` (copy it to the new location first to act as the baseline).

Ensure your Rust tool compiles correctly and your pipeline standard stream redirections properly separate standard output (clean logs) from standard error (if any).