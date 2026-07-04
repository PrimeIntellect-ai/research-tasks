You are an incident responder investigating a localized credential leak on a Linux system. A vulnerable process named `vuln_service` is running multiple instances on the system under your user account. It is known that this service accepts sensitive credentials as command-line arguments via the `--secret` flag, which makes them visible in the `/proc` filesystem.

Your task is to automate the discovery of these leaked secrets and set up secure access for the rest of the incident response (IR) team.

Perform the following steps:
1. Write a C program located at `/home/user/scanner.c`. This program must:
   - Iterate through the `/proc` directory.
   - Identify all running processes with the exact name `vuln_service`.
   - Read their command-line arguments (e.g., from `/proc/[pid]/cmdline`).
   - Extract the value passed to the `--secret` argument.
   - Write these extracted secret strings to a log file at `/home/user/extracted_secrets.log`. The secrets in this file must be sorted alphabetically, with one secret per line.
2. Compile your C program and run it to generate the `/home/user/extracted_secrets.log` file.
3. Secure the system for the IR team by generating an Ed25519 SSH key pair. Save the key pair to `/home/user/.ssh/ir_key` (do not use a passphrase).
4. Add the newly generated public key to `/home/user/.ssh/authorized_keys`. However, to harden the access, you must prepend the `restrict` option to the key entry in the `authorized_keys` file (e.g., `restrict ssh-ed25519 AAA...`).

Ensure that the output file `/home/user/extracted_secrets.log` exactly matches the required format and that the SSH key is correctly generated and added with the specified restriction.