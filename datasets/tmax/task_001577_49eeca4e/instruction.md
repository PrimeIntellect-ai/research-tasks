You are a QA engineer tasked with replacing an outdated, proprietary log sanitizer with a modern C++ implementation. You must build a new filter that perfectly matches the behavior of the legacy system, while fixing build issues and modernizing the codebase.

We have a legacy, stripped binary located at `/app/legacy_filter`. It reads a single line from standard input and exits with code `0` if the log line is "clean", or code `1` if the log line is "evil" (malicious or contains sensitive data). 

Your workspace is located at `/home/user/workspace/`. It contains:
1. A buggy `Makefile` that currently fails to compile.
2. A legacy C prototype file `old_logic.c` which implements *part* of the sanitization logic.
3. A skeleton C++ file `main.cpp`.
4. A small sample corpus in `/home/user/corpus/clean/` and `/home/user/corpus/evil/`.

Your tasks:
1. **Fix the Makefile**: Repair `/home/user/workspace/Makefile` so that running `make` successfully compiles `main.cpp` into an executable named `log_filter`.
2. **Translate and Extend**: Translate the logic from `old_logic.c` into modern C++ in `main.cpp`. 
3. **Reverse-Engineer the Oracle**: The provided `old_logic.c` is incomplete. Use the stripped binary `/app/legacy_filter` as a black-box oracle to deduce the missing filtering rules. 
4. **Implement the Filter**: Your compiled `/home/user/workspace/log_filter` must process a log file via standard input (e.g., `cat input.log | ./log_filter`). It must print "clean" lines to standard output exactly as they appeared, and completely drop/ignore "evil" lines.

Verification:
Your `log_filter` executable will be tested against a large, secret adversarial corpus containing both clean and evil logs. To succeed, your program must output 100% of the clean lines unmodified and omit 100% of the evil lines.

Constraints:
- Do not modify the `/app/` directory.
- Your final executable must be located at `/home/user/workspace/log_filter`.
- Handle inputs line by line.