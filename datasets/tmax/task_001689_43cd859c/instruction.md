You are a platform engineer maintaining a high-throughput CI/CD pipeline. One of our build steps uses a Python script, `/home/user/legacy_hasher.py`, to parse, filter, and hash deployment artifact names from a stream of log lines. Because of increasing log volumes, this Python script has become a critical bottleneck. 

Your task is to port this script to C++ to dramatically improve its performance, utilizing a vendored version of the `xxHash` C library.

**Task Requirements:**

1. **Fix and Build the Vendored Dependency:**
   We have vendored the source code for `xxHash-0.8.2` in `/app/vendored/xxHash-0.8.2`. However, a previous developer accidentally broke its `Makefile` while trying to refactor the build system. As a result, the static library (`libxxhash.a`) fails to build correctly (the archive step silently fails or uses the wrong command). 
   - Identify and fix the perturbation in `/app/vendored/xxHash-0.8.2/Makefile`.
   - Run `make` to successfully build `libxxhash.a`.

2. **Code Translation:**
   Translate the logic of `/home/user/legacy_hasher.py` into a C++ program.
   - The C++ source must be written to `/home/user/fast_hasher.cpp`.
   - It must read from `stdin` (one line at a time) and write to `stdout`.
   - It must utilize the `#include "xxhash.h"` header and link against your freshly built `libxxhash.a`.
   - The output must be **bit-exact** equivalent to the Python script for any arbitrary standard input.

3. **Compilation:**
   Compile your C++ program using `g++`:
   - Output executable must be exactly at: `/home/user/fast_hasher`
   - You must statically link the vendored `libxxhash.a`.

*Note: The automated verification system will randomly fuzz your `/home/user/fast_hasher` executable against millions of generated lines to ensure absolute bit-exact equivalence with the original script.*