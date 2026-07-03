You are managing a binary artifact repository. You regularly receive backup archives containing compiled binaries, consisting of a base archive and several incremental updates. Some of these archives might be improperly packaged or maliciously crafted to extract files outside the target directory (a "zip slip" vulnerability).

Your task is to write a Bash script at `/home/user/curate_artifacts.sh` that safely processes these archives, applies the valid incremental backups, and organizes the resulting binaries.

The incoming archives are located in `/home/user/incoming/` and are named sequentially, e.g., `1_base.tar`, `2_inc.tar`, `3_inc.tar`.

Your script must perform the following actions automatically when executed:

1. **Security & Integrity Check:** 
   Iterate through all `.tar` files in `/home/user/incoming/` in alphabetical order. 
   For each archive, inspect its contents without extracting it. If any file path in the archive starts with `/` (absolute path) or contains `../` (parent directory traversal), the archive must be considered malicious.
   - If an archive is malicious, do NOT extract it. Append the exact string `REJECTED: <filename>` (e.g., `REJECTED: 2_inc.tar`) to `/home/user/curation.log`.
   - If an archive is safe, append `ACCEPTED: <filename>` to `/home/user/curation.log`.

2. **Incremental Extraction:**
   For all *safe* archives, extract their contents into `/home/user/repo/` in alphabetical order. (Extracting them sequentially ensures newer incremental files correctly overwrite older ones). Ensure the directory `/home/user/repo/` exists before extracting.

3. **ELF Parsing & Bulk Renaming:**
   After all safe archives have been extracted, find all files in `/home/user/repo/` (recursively) that are ELF binaries.
   Analyze each ELF binary using the `file` command to determine its architecture.
   - If the `file` command output contains `x86-64`, rename the file by appending `_x86_64` to its name (e.g., `app` becomes `app_x86_64`).
   - If the `file` command output contains `aarch64`, rename the file by appending `_aarch64`.
   - If the `file` command output contains `ARM`, but not `aarch64`, rename by appending `_arm`.
   - If the `file` command output contains `386`, rename by appending `_i386`.

You must only use Bash, coreutils, and standard Linux utilities (like `tar`, `file`, `find`, `grep`). 
Run your script once you have written it to ensure `/home/user/repo/` is populated correctly and `/home/user/curation.log` is generated.