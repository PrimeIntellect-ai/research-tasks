You are a compliance analyst generating an automated audit trail for a legacy web server deployment. The deployment consists of an executable binary and a TLS certificate. You need to verify the binary's integrity and the certificate's validity window.

You have been provided with two files:
1. `/home/user/server_bin` (The executable ELF binary)
2. `/home/user/server.crt` (The X.509 TLS certificate)

Perform the following tasks to generate the compliance audit report:

1. **Write a C program** at `/home/user/elf_audit.c` that takes a file path as its first command-line argument, reads its 64-bit ELF header (`Elf64_Ehdr`), and prints the entry point address (`e_entry`) exactly in the following format: `Entry: 0x[address in lowercase hex]`. 
   Compile this program to `/home/user/elf_audit`.
   *(Hint: Use `<elf.h>` and standard I/O functions. Assume the target is always a valid 64-bit ELF).*

2. **Extract the expiration date** of the TLS certificate `/home/user/server.crt` using standard command-line tools (e.g., `openssl`).

3. **Generate an audit report** at `/home/user/audit_report.txt`. The file must contain exactly two lines:
   - Line 1: The output of your `/home/user/elf_audit` program when run against `/home/user/server_bin`.
   - Line 2: The expiration date of the TLS certificate in the format: `Expiry: [date string as output by openssl enddate]`. (For example: `Expiry: May 10 12:00:00 2025 GMT`).

Ensure the final report exists at `/home/user/audit_report.txt` with the exact requested formatting.