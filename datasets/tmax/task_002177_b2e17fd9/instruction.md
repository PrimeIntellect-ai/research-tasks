You are helping a developer organize their chaotic project files. They recently tried to back up their project directory, but their Python backup script got stuck in an infinite loop due to cyclic symlinks and crashed. 

Your task involves cleaning up the directory, redacting sensitive information, and fixing the backup script to safely archive the project.

Here are your specific objectives:

1. **Identify and Remove Cyclic/Broken Symlinks:**
   Analyze the directory `/home/user/project_root`. Find any broken or cyclic symlinks.
   Save the absolute paths of these problematic symlinks to a log file at `/home/user/bad_links.txt` (one path per line, sorted alphabetically). Once logged, delete the broken/cyclic symlinks from the filesystem.

2. **Redact Sensitive Information:**
   Find all `.conf` files within `/home/user/project_root` and its subdirectories. 
   Transform the text in these files in-place: whenever a line starts with `PASSWORD=`, replace the entire line with `PASSWORD=REDACTED`. You can use standard Linux tools (like `sed`, `awk`) or Python for this.

3. **Fix the Backup Script:**
   The developer left a broken Python backup script at `/home/user/backup_script.py`. It currently uses `os.walk` with `followlinks=True`, causing infinite loops, and it doesn't filter files correctly.
   Modify `/home/user/backup_script.py` so that:
   - It **does not** follow symlinks (prevents infinite loops).
   - It collects all regular files and *valid* symlinks.
   - It writes the valid symlinks it encountered to `/home/user/skipped_symlinks.log` (absolute paths, one per line, sorted alphabetically).
   - It packages the regular files and directories into a compressed tarball at `/home/user/safe_archive.tar.gz`.

4. **Run the Script:**
   Execute your fixed script so that `/home/user/safe_archive.tar.gz` and `/home/user/skipped_symlinks.log` are generated successfully.

Ensure all file paths in the text files (`bad_links.txt`, `skipped_symlinks.log`) are absolute paths.