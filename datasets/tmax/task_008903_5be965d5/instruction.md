You are a security auditor tasked with performing automated vulnerability scanning, privilege escalation auditing, and ELF binary analysis. You need to write a custom C++ tool to inspect a collection of compiled binaries for specific security risks.

The directory `/home/user/targets` contains several ELF executables. Some of these binaries may have excessive permissions (setuid) and may contain hardcoded sensitive file paths in their read-only data sections, indicating a potential vulnerability.

Your task is to:
1. Write a C++ program at `/home/user/vuln_scanner.cpp` that iterates through all files in the directory `/home/user/targets`.
2. For each file, verify that it is a valid 64-bit ELF executable.
3. Check the file's permissions to determine if the setuid (SUID) bit is set.
4. Parse the ELF structures natively to locate the `.rodata` (read-only data) section. You must do this by reading the ELF header, finding the section header string table, and iterating through the section headers to find the one named `.rodata`.
5. Search exclusively within the bounds of the `.rodata` section for the exact null-terminated string `/etc/shadow`.
6. Output the findings for each file to `/home/user/scan_results.txt`. The output must be sorted alphabetically by filename, with one file per line in the following exact format:
   `<filename>: SUID=<Yes/No>, SHADOW_IN_RODATA=<Yes/No>`

Constraints:
- Do not use external libraries for ELF parsing (such as `libelf`). You must parse the binary format manually using standard C++ features and the definitions provided in `<elf.h>`.
- Compile your program using `g++ -std=c++17 /home/user/vuln_scanner.cpp -o /home/user/vuln_scanner`.
- Run your compiled program to generate the `/home/user/scan_results.txt` file.

Example output format for `/home/user/scan_results.txt`:
```
fake_bin: SUID=Yes, SHADOW_IN_RODATA=No
safe_bin: SUID=No, SHADOW_IN_RODATA=No
suid_bin: SUID=Yes, SHADOW_IN_RODATA=Yes
```