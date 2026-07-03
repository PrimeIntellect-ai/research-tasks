As a storage administrator, we are migrating off an ancient proprietary backup system to reclaim disk space. Our legacy backups were compressed using a custom, closed-source utility. We have the binary for this utility located at `/app/legacy_packer`, but it is stripped, unsupported, and we want to replace it entirely with a maintainable Python implementation. 

Your task is to:
1. Reverse-engineer the behavior of the `/app/legacy_packer` binary. The binary reads raw data from `stdin`, compresses it using a specific standard algorithm (like zlib or gzip), adds custom headers/footers, calculates a checksum, and writes the resulting binary format to `stdout`.
2. Write a Python script at `/home/user/packer.py` that replicates this behavior perfectly. Your script must read from standard input and write the exact same custom packed format to standard output. 
3. Your implementation must be bit-exact equivalent to the `/app/legacy_packer` binary for ANY arbitrary input stream (text or binary).
4. Ensure your script handles standard stream redirection and piping efficiently.

Constraints:
- Your script must be executable via `python3 /home/user/packer.py`.
- Do not use any third-party pip packages; rely on Python's standard library (e.g., `sys`, `struct`, `zlib`, `hashlib`, etc.).
- Analyze the binary carefully (you can use `strings`, `xxd`, `strace`, or pipe sample data through it) to understand the magic bytes, endianness of the length/checksum fields, and the exact compression settings used.

Write the `/home/user/packer.py` file. I will verify your solution by fuzzing it with thousands of random inputs and comparing the output bytes to the legacy binary.