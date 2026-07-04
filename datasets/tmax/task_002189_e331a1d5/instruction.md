You are a mobile build engineer maintaining an older build pipeline for a custom Android application. 

As part of our migration to a new 64-bit multi-platform architecture, we are eliminating opaque precompiled blobs from our build tree. We have one remaining legacy utility located at `/app/legacy_packer`. This executable is a stripped, compressed binary that processes application asset files. The original C source code and the custom data structures it utilized were lost years ago. We know it processes raw byte streams through standard input and produces transformed bytes to standard output, but the exact compression or obfuscation ABI it applies is undocumented.

Your task is to:
1. Reverse-engineer the `/app/legacy_packer` executable to understand the custom algorithm it applies to the incoming byte stream. (Tools like `objdump`, `gdb`, `strings`, and `upx` are available).
2. Design and implement a completely equivalent, clean Python 3 script at `/home/user/packer.py`.
3. Your Python script must read from `stdin`, process the bytes using the exact same logic and custom block handling as the legacy binary, and write the result to `stdout`.
4. Ensure your script is highly efficient and handles arbitrary binary data without crashing or buffering indefinitely. It must act as a perfect, bit-exact drop-in replacement for the legacy binary.

Your script will be verified by a fuzzing harness that blasts both `/app/legacy_packer` and `/home/user/packer.py` with identical random binary data and asserts that the `stdout` streams match perfectly byte-for-byte. 

Make sure `/home/user/packer.py` is executable (`chmod +x`) and begins with `#!/usr/bin/env python3`.