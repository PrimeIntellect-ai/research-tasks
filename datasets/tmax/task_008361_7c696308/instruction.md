You are a compliance analyst tasked with generating an audit trail for a recent security incident and patching the affected service. 

We have a legacy file upload utility written in C. Recently, we suspect an attacker bypassed the intended directory restrictions and overwrote a sensitive file on the system.

You have been provided with the following in `/home/user/`:
1. `upload_handler.c`: The source code of the vulnerable upload utility.
2. `upload.log`: The service access logs.
3. `uploads/`: The intended directory for all uploaded files.

Perform the following tasks:

**Part 1: Audit Report**
Analyze the C code and the log file to identify the vulnerability and the breach. Create an audit report at `/home/user/audit_report.txt` with exactly the following three lines:
- Line 1: The precise CWE ID of the vulnerability present in the C code (e.g., `CWE-XXX`).
- Line 2: The IP address of the attacker who successfully exploited this vulnerability, according to `upload.log`.
- Line 3: The SHA-256 hash of the maliciously uploaded file (you will need to find where it was written on the file system based on the log and hash it).

**Part 2: Remediation**
Patch the `/home/user/upload_handler.c` file to securely validate the input. 
- The patched program must reject any filename that contains a forward slash (`/`) or the string `..`.
- If an invalid filename is detected, the program must print "Invalid filename" to standard error and exit with status code `1` immediately, without writing any files.
- If the filename is valid, it should proceed to write the file into the `uploads/` directory just like the original code and exit with status `0`.
- Compile your patched code to an executable named `/home/user/upload_handler_patched` using `gcc`.

Ensure your patched binary functions correctly, as it will be executed with various test inputs during verification.