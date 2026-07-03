You are an incident responder investigating a compromised Linux system. A custom C utility used to process data uploads was exploited to write files outside of its intended directory. 

Your task is to investigate the breach, patch the vulnerable software, and identify the malicious files.

Here are your instructions:
1. **Code Audit & Patching**: Inspect `/home/user/upload_processor.c`. The program is designed to accept a filename and content as arguments, and write the content to `/home/user/data/<filename>`. However, it is vulnerable to Path Traversal (CWE-22). 
   Modify the C code so that if the provided `filename` argument contains the character `/` or the sequence `..`, the program prints exactly "Invalid filename\n" to standard error and exits with code 1 without writing any files.
2. **Compilation & Permissions**: Compile the patched source code to an executable at `/home/user/processor_secure`. Secure the binary by setting its file permissions to exactly `750` (read/write/execute for owner, read/execute for group, no permissions for others).
3. **Integrity & File Discovery**: The attacker used the vulnerability to write `.txt` files outside of the intended `/home/user/data/` directory, but somewhere within `/home/user/`. 
   Find all `.txt` files in `/home/user/` (and its subdirectories) that are *not* inside `/home/user/data/` (or its subdirectories). 
   Calculate the SHA-256 hashes of these rogue files.
4. **Reporting**: Write the hash results to `/home/user/malicious_files.log`. The format must exactly match the default output of the `sha256sum` command (e.g., `<hash>  <absolute_filepath>`). Sort the lines of this log file alphabetically by the absolute file path.

Ensure the final patched binary compiles successfully and securely handles malicious inputs.