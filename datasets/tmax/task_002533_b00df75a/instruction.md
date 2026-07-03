You are a security researcher investigating a new malware strain. We have recovered a stripped binary, `/app/oracle.bin`, which appears to be a custom mathematical data transformation tool (possibly a custom hash or obfuscation routine) used by the malware to decode its payloads. 

We also obtained a small ext4 filesystem image from the attacker's server: `/app/evidence.img`. Forensics suggest that the attacker accidentally saved and then immediately deleted a slightly older, buggy version of the C source code for this algorithm on that filesystem.

Your objectives are:
1. **Recover the source code:** Inspect the `/app/evidence.img` filesystem (you may need to use tools like `debugfs`, `fls`, or `icat`) and recover the deleted C source file (originally named `obfuscator.c`). Save it to `/home/user/obfuscator.c`.
2. **Diagnose and fix the build:** The recovered code has a few syntax and type errors preventing it from compiling. Fix these build failures.
3. **Trace and fix runtime errors:** The recovered code contains format parsing edge-case bugs (it fails or crashes on inputs containing specific null-byte patterns) and uses uninitialized memory, leading to intermittent failures. Use a debugger or intermediate state tracing to find and repair these issues.
4. **Achieve exact equivalence:** The final compiled C program must be bit-for-bit functionally equivalent to the stripped binary `/app/oracle.bin`. Both programs take exactly 64 bytes of raw binary data from `stdin` and output exactly 64 bytes of transformed data to `stdout`. 

Compile your final corrected source code to an executable located exactly at:
`/home/user/solution`

It must be compiled dynamically or statically for a standard Linux x86_64 environment, and read from standard input, writing to standard output.