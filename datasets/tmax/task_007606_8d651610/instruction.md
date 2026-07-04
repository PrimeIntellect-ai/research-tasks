You are managing a configuration system that accepts configuration updates as `.tar` archives. Recently, you discovered that some submitted archives are corrupted, and others contain malicious path traversals (Zip Slip attacks) attempting to overwrite files outside the target directory (e.g., using absolute paths like `/etc/passwd` or relative paths like `../config.json`).

Your task is to create a C++ program that analyzes these incoming archives, verifies their integrity, checks for directory traversal attacks, and categorizes them using file links.

Here are your instructions:

1. **Environment:**
   - Incoming archives are located in `/home/user/incoming_configs/`.
   - You must place safe archives in `/home/user/safe_configs/`.
   - You must place malicious archives in `/home/user/quarantine_configs/`.
   - You must log corrupted archives to `/home/user/corrupted.log`.

2. **Write a C++ program at `/home/user/config_filter.cpp`** that performs the following logic:
   - Iterate through all `.tar` files in `/home/user/incoming_configs/`.
   - For each archive, use standard stream redirection/piping (e.g., via `popen`) to execute `tar -tf <archive_path>`.
   - **Archive Integrity Verification:** If the `tar` command fails (non-zero exit status), the archive is corrupted. The program should output the base filename (e.g., `bad.tar`) to standard error (`std::cerr`).
   - **Zip Slip Detection:** If the archive is valid, parse the output of `tar -tf`. If ANY file path in the archive starts with a forward slash (`/`) or contains the string `../`, it is considered malicious.
   - **Link Management:**
     - If the archive is safe (valid and not malicious), create a **hard link** to the archive in `/home/user/safe_configs/` keeping the same base filename.
     - If the archive is malicious, create a **symbolic link** to the archive in `/home/user/quarantine_configs/` keeping the same base filename.
     - Do not create any links for corrupted archives.

3. **Execution & Redirection:**
   - Compile your program to `/home/user/config_filter`.
   - Run the program. You must redirect its standard error stream to create the `/home/user/corrupted.log` file, ensuring the file only contains the base filenames of the corrupted archives, one per line.

Ensure the final state of the `/home/user/safe_configs/` and `/home/user/quarantine_configs/` directories precisely reflects the categorization using the correct link types.