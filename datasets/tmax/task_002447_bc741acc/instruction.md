You are a developer tasked with organizing and modernizing legacy project files. You have been receiving continuous drops of compressed archives containing old source code, but the files are encoded in legacy character sets and need to be modernized on the fly.

Your objective is to create a Bash-only background daemon script that watches a directory, processes compressed archives, converts specific files, and moves them to an output directory.

**Requirements:**

1. **Directories**: 
   - Watch directory: `/home/user/incoming`
   - Output directory: `/home/user/outgoing`
   - Staging directory (already exists with test files): `/home/user/staging`
   You must create `/home/user/incoming` and `/home/user/outgoing`.

2. **The Daemon Script (`/home/user/organizer.sh`)**:
   - Write a Bash script at `/home/user/organizer.sh`.
   - The script should run continuously in the background (using an infinite loop with a `sleep 2` pause to avoid high CPU usage).
   - It should monitor `/home/user/incoming` for any new `.tar.gz` files.
   - For every `.tar.gz` file found, it must:
     a. Extract the archive into a secure, newly created temporary directory.
     b. Recursively find all files with the `.src` extension.
     c. Convert the character encoding of all found `.src` files from `ISO-8859-1` to `UTF-8` in-place (or overwrite them so the new UTF-8 file replaces the old one). Non-`.src` files must be left completely untouched.
     d. Create a new `.tar.gz` archive of the transformed contents and place it in `/home/user/outgoing/` with the exact same base filename. *Note: The internal directory structure of the new archive must perfectly match the original archive (i.e., don't wrap it in an extra temporary directory folder).*
     e. Count the total number of `.src` files that were successfully converted.
     f. Append a log entry to `/home/user/organizer.log` in this exact format:
        `PROCESSED: <filename> | CONVERTED_FILES: <count>`
        (e.g., `PROCESSED: code_drop.tar.gz | CONVERTED_FILES: 4`)
     g. Delete the processed `.tar.gz` file from `/home/user/incoming`.

3. **Execution and Verification**:
   - Make your script executable.
   - Start the script in the background.
   - To test your script and complete the task, copy all `.tar.gz` files from `/home/user/staging/` into `/home/user/incoming/`.
   - Wait a few seconds for your background script to process them.
   - Verify that `/home/user/outgoing/` contains the processed archives, `/home/user/incoming/` is empty, and `/home/user/organizer.log` contains the correct entries.

Do not use external dependencies outside of standard coreutils, `tar`, `gzip`, and `iconv`. Do not use `inotifywait` (rely on standard bash polling).