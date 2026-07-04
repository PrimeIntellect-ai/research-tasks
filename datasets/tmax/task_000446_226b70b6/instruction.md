You are a build engineer responsible for artifact management. We have a pipeline that parses artifact metadata using a lightweight INI format. 

Currently, our pipeline is broken due to two issues:
1. The upstream vendored INI parsing library we use (`inih`, located at `/app/vendor/inih-53`) fails to build because its `Makefile` was accidentally corrupted during a messy merge.
2. We lost the source code for the metadata normalizer tool, `artifact_parser`. We only have a stripped compiled binary of it located at `/app/oracle_parser`.

Your tasks:
1. **Fix the Vendored Package:** Inspect `/app/vendor/inih-53/Makefile`. It has a deliberate error preventing `libinih.a` from compiling. Fix the Makefile and run `make` to produce `libinih.a`.
2. **Recreate the Parser:** Write a new C program at `/home/user/artifact_parser.c` that links against `/app/vendor/inih-53/libinih.a` and `#include "ini.h"`.
3. **Match the Oracle:** Your compiled `/home/user/artifact_parser` must read an INI-formatted string from standard input (stdin) until EOF, and print the parsed key-value pairs to standard output (stdout) in exactly the same format as `/app/oracle_parser`. 

The output format of the oracle is:
`[section] key=value\n`
for every valid key-value pair parsed. If the input is invalid, it simply prints nothing for the invalid parts and continues, matching standard `inih` behavior.

Compile your program exactly to `/home/user/artifact_parser`. Our automated verification will generate thousands of random INI files, feed them to both your `artifact_parser` and the `oracle_parser`, and assert that the byte-for-byte output is strictly identical (Fuzz equivalence). 

Ensure your C code is robust against standard fuzzing inputs (e.g., malformed sections, long strings, unexpected characters).