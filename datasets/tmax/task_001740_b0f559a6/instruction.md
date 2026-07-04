You are tasked with debugging a failing build for our database recovery pipeline and implementing a sanitizer to prevent malicious payloads from triggering memory corruption in our proprietary validation tool.

**Stage 1: Fix the Vendored Package Build**
We rely on a vendored package, `libwalrec`, located at `/app/libwalrec`. Currently, if you run `make` inside that directory, the build fails. 
1. Diagnose and fix the build issue. The objective is for `make` to successfully compile the library into `libwalrec.a`. You may modify the Makefile or source files in `/app/libwalrec` as necessary to make it build cleanly.

**Stage 2: Reverse Engineer the Validation Binary**
We use an internal binary, `/app/bin/wal_checker`, to validate the Write-Ahead Log (WAL) files. Recently, we discovered that certain corrupted WAL files cause `wal_checker` to crash with a segmentation fault or assertion failure due to memory corruption.
1. Inspect the `/app/bin/wal_checker` binary using reverse engineering tools (like `objdump`, `gdb`, or `strings`).
2. Deduce the specific conditions under which a WAL record triggers the crash. 
*Hint:* The WAL format consists of a 4-byte magic header (`WAL1`), followed by a sequence of records. Each record has a 1-byte 'type', a 2-byte 'length' (little-endian), and a payload of 'length' bytes.

**Stage 3: Develop the WAL Sanitizer**
Write a C program that inspects WAL files and rejects those that exploit the vulnerability you discovered in `wal_checker`.
1. Create your source code at `/home/user/wal_sanitizer.c`.
2. Compile it to an executable at `/home/user/wal_sanitizer`.
3. The executable must accept exactly one argument: the file path to a WAL file (e.g., `/home/user/wal_sanitizer /path/to/file.wal`).
4. If the WAL file contains *any* record that would trigger the crash/vulnerability in `wal_checker`, your program must terminate with an exit code of `1` (rejected).
5. If the WAL file is well-formed and safe for `wal_checker` to process, your program must terminate with an exit code of `0` (accepted).

Ensure your sanitizer processes the entire file and strictly adheres to the return code requirements.