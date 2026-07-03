You are an infrastructure engineer tasked with automating a secure backup provisioning pipeline. Your goal is to write a C-based utility, configure a TLS-secured local file server, and orchestrate the entire process using a CI/CD-style bash shell script.

You have access to a standard non-root Linux environment. The home directory is `/home/user`.

Perform the following steps:

1. **Environment Setup:**
   - Create the following directories: `/home/user/app_data`, `/home/user/backups`, and `/home/user/certs`.
   - Create a dummy file named `/home/user/app_data/config.txt` containing the text: `db_port=5432`.
   - Ensure `/home/user/backups` has restrictive permissions so that only the owner can read, write, or execute it (`chmod 700`).

2. **TLS Configuration:**
   - Generate a self-signed RSA 2048-bit TLS certificate and private key valid for 365 days.
   - Save the certificate to `/home/user/certs/server.crt` and the private key to `/home/user/certs/server.key`.
   - The private key must have strict permissions (`600`).

3. **C-based Backup Utility:**
   - Write a C program and save it to `/home/user/backup_tool.c`.
   - The program must take exactly two command-line arguments: `<source_directory>` and `<destination_archive>`.
   - Using the `stat()` system call from `<sys/stat.h>`, the program must first check if the `<source_directory>` exists. If it does not exist, print an error to stderr and return an exit status of `1`.
   - If the directory exists, use the `system()` function to execute a command that creates a `.tar.gz` archive of the `<source_directory>` at the `<destination_archive>` path. 
   - If the backup succeeds, return `0`.

4. **Pipeline Automation Script:**
   - Write a bash script named `/home/user/pipeline.sh` that automates the build, execution, and deployment phases.
   - The script must perform the following actions sequentially:
     a. Compile `/home/user/backup_tool.c` into an executable named `/home/user/backup_tool` using `gcc`.
     b. Execute the compiled `backup_tool` to backup `/home/user/app_data` into `/home/user/backups/latest.tar.gz`.
     c. Start a secure web server in the background using `openssl s_server` to serve the contents of `/home/user/backups` over HTTPS on port `8443`. (Hint: use the `-WWW` flag, provide the cert and key generated earlier, and ensure it runs from within `/home/user/backups`).
     d. Append the exact string `DEPLOYMENT SUCCESS` to a log file located at `/home/user/deploy.log`.

5. **Execution:**
   - Run your `/home/user/pipeline.sh` script to execute the pipeline and leave the server running.

Verify that your pipeline successfully created the backup archive and that the secure server is listening on port 8443.