You are a network engineer tasked with inspecting a packet capture embedded in an executable file, while ensuring strict security protocols. 

You have been provided with an ELF object file `/home/user/capture.o` which contains a custom section named `.traffic_dump`. This section contains proprietary network traffic records. 

Additionally, you have a Root Certificate Authority file at `/home/user/rootCA.pem`.

Your task requires you to perform the following steps:

1. **ELF Analysis**: Extract the raw binary contents of the `.traffic_dump` section from `/home/user/capture.o` to a file named `/home/user/dump.bin`.

2. **C Program for Secure Processing**: Write a C program at `/home/user/processor.c` that parses `/home/user/dump.bin`.
   - **Process Isolation**: The program must sandbox itself using `libseccomp`. Open any necessary files before applying the seccomp filter. The filter must be strictly configured to allow ONLY the `read`, `write`, `close`, `fstat`, `mmap`, `munmap`, `brk`, `exit`, and `exit_group` syscalls (kill the process on any other syscall).
   - **Format Parsing**: The binary dump consists of multiple sequential records. Each record has:
     - 2-byte Record ID (unsigned short, little-endian)
     - 2-byte Length (unsigned short, little-endian)
     - Data Payload (Length bytes)
   - **Sensitive Data Redaction**: As the program reads the payloads, it must redact credit card numbers (any sequence of exactly 16 digits) by replacing all 16 digits with the character `X`. It must also redact Social Security Numbers matching the exact pattern `SSN: ddd-dd-dddd` (where `d` is a digit) by replacing the digits with `X` (resulting in `SSN: XXX-XX-XXXX`).
   - **Output**: The C program must concatenate all redacted payloads (in order) and write them to `/home/user/redacted_traffic.log`.
   - **Certificate Extraction**: Some payloads are PEM-formatted certificates (starting with `-----BEGIN CERTIFICATE-----`). The C program must extract these payloads and save them to the directory `/home/user/certs/` with the filename `<Record ID>.pem` (e.g., `5.pem`). Create the `/home/user/certs/` directory before running your program.

3. **Vulnerability Scanning**: Run the `cppcheck` tool on your `processor.c` code to ensure there are no obvious flaws. Save the output to `/home/user/cppcheck.log` using the command: `cppcheck --enable=all processor.c > /home/user/cppcheck.log 2>&1`.

4. **Certificate Chain Validation**: Using `bash` and the `openssl` command-line tool, verify the extracted certificates in `/home/user/certs/` against the provided `/home/user/rootCA.pem`. Write the Record IDs (just the numbers, one per line, sorted numerically) of the certificates that successfully validate to `/home/user/valid_certs.log`.

Compile your C program with `gcc -o /home/user/processor /home/user/processor.c -lseccomp` and execute it to generate the required outputs. Ensure all files mentioned are exactly at the specified paths.