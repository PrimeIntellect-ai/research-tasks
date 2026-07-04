You are a security auditor tasked with reviewing and securing a custom C-based file upload handler. The application decodes base64 payloads and writes them to an uploads directory, but it is suspected to have a path traversal vulnerability. 

The application is located in `/home/user/uploader`.
Inside this directory, you will find `uploader.c` and an `uploads` directory.

Perform the following tasks:

1. **File Integrity Verification**: Compute the SHA256 hash of the original `/home/user/uploader/uploader.c` file and save the hash (just the hash string, no filenames) to `/home/user/audit_hash.txt`.

2. **Payload Encoding & Exploit PoC**: The compiled program (`./uploader`) takes two arguments: a filename and a base64-encoded payload. It writes the decoded payload to `uploads/<filename>`. 
Create a bash script at `/home/user/poc.sh` that runs the existing compiled `/home/user/uploader/uploader` binary to write the exact text `EXPLOIT_SUCCESS` to the file `/home/user/target.txt` (outside the uploads directory) by exploiting the path traversal vulnerability. The script must handle the base64 encoding of the payload dynamically.

3. **Secure Coding**: Edit `/home/user/uploader/uploader.c` to patch the vulnerability. Add input validation to the filename argument. If the filename contains a forward slash (`/`) or a dot (`.`), the program must print `Access Denied` to stdout and immediately exit with status code 1. 

4. **Compilation**: Compile your patched C code and output the executable to `/home/user/uploader_fixed`. (Do not overwrite the original binary).

5. **File Permission & Access Control**: The `uploads` directory currently has insecure permissions. Change the permissions of `/home/user/uploader/uploads` so that only the owner has read, write, and execute permissions (drwx------).

Ensure all scripts are executable where appropriate, and all output files are placed exactly at the specified paths.