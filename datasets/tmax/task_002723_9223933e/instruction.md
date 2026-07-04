You are a cloud architect migrating an old backup and storage monitoring stack to a new environment. You need to accomplish three distinct tasks to restore the storage workflow.

**Step 1: Audio Memo Extraction**
Listen to the legacy dictation file located at `/app/migration_memo.wav`. It contains a short spoken sentence specifying the secret target directory name for our new backup schema. You must determine this directory name (it will be two words, e.g., "project alpha"). Use `whisper-cli` or `ffmpeg` to process it if you need.

**Step 2: Fix the Systemd Backup Service**
We have a local systemd user service at `~/.config/systemd/user/storage-sync.service` which pushes backups over an SSH tunnel. It currently fails to run reliably on boot because it attempts to connect before the SSH tunnel service (`ssh-tunnel.service`) is ready. 
Modify `storage-sync.service` to correctly specify that it must start *After* `ssh-tunnel.service` and that it *Requires* it. Once modified, reload the systemd user daemon, and enable and start `storage-sync.service`.

**Step 3: Re-implement the Legacy Path Sanitizer in Go**
We use a binary to sanitize and map messy user-provided filepaths to their absolute backup storage locations on the disk quota system. The legacy binary is closed-source. You must write a replacement in Go at `/home/user/src/path_sanitizer.go` and compile it to `/home/user/bin/path_sanitizer`.

The Go program must read a raw filepath from `stdin` (until EOF) and print the normalized path to `stdout` with NO trailing newline.
The strict sanitization rules (which must perfectly match the old binary's behavior) are:
1. Strip all leading and trailing whitespace from the entire input.
2. Convert all letters to lowercase.
3. Replace all spaces (` `) with hyphens (`-`).
4. Remove any character that is NOT in the following set: `[a-z]`, `[0-9]`, `-`, `_`, `/`, `.`.
5. Replace any sequences of multiple consecutive slashes (e.g., `///`) with a single slash `/`.
6. Ensure the sanitized string starts with a single slash `/` (if it doesn't already, add one. If it's completely empty after cleaning, it becomes `/`).
7. Prepend the absolute backup prefix: `/storage/backups/{DIR_NAME}` where `{DIR_NAME}` is the directory name you transcribed from the audio in Step 1 (formatted in lowercase, with spaces replaced by underscores). 
For example, if the audio said "project nebula", the prefix is `/storage/backups/project_nebula`. Thus, an input of "  My Weird  File.txt " becomes `/storage/backups/project_nebula/my-weird--file.txt`.

Ensure your Go program precisely matches these rules, as it will be rigorously tested against millions of random inputs against our reference implementation.