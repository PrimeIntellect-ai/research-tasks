You are an artifact manager responsible for safely curating legacy binary repositories. You have received an archive file located at `/home/user/artifacts.tar` that needs to be extracted, sanitized, and organized.

Please perform the following operations using Bash shell commands and scripts:

1. **Safe Extraction and Sanitization:**
   - Create a directory called `/home/user/curated_repo` and extract the contents of `/home/user/artifacts.tar` directly into it.
   - The archive is suspected of containing a "Zip Slip" style vulnerability via symbolic links. Find and delete any extracted file or symlink in `/home/user/curated_repo` that resolves to a target *outside* of `/home/user/curated_repo` (e.g., pointing to system files like `/etc/passwd`). Keep all safe files and valid internal symlinks.

2. **Character Encoding Conversion:**
   - Find all `.txt` files within `/home/user/curated_repo`. 
   - These legacy text files are encoded in `ISO-8859-1`. Convert their contents to `UTF-8` encoding and overwrite the original files with the converted content.

3. **Bulk File Renaming:**
   - Find all `.bin` files in the repository.
   - Rename them in bulk by replacing any space characters (` `) in their filenames with underscores (`_`), and change their file extensions from `.bin` to `.elf`. (For example, `my tool.bin` should become `my_tool.elf`).

4. **Link Management (Hard and Symbolic Links):**
   - Create a new directory at `/home/user/curated_repo/release`.
   - Create **hard links** for all of the newly renamed `.elf` files inside the `/home/user/curated_repo/release` directory.
   - Create a **symbolic link** at `/home/user/curated_repo/latest` that points exactly to the `release` directory (`/home/user/curated_repo/release`).

5. **Verification Log:**
   - Create a log file at `/home/user/audit.log` containing only the basenames of the files present in `/home/user/curated_repo/release/`, sorted alphabetically, with one filename per line.

Ensure you do not use `su` or root permissions, as you only have standard user access.