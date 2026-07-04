**TICKET ID:** #IT-8832-CRASH
**STATUS:** OPEN
**SUBJECT:** Legacy proprietary parser crashing in production
**DESCRIPTION:**

Hello Support,

We have a legacy internal tool located at `/app/legacy_parser` that processes incoming binary telemetry payloads. Unfortunately, the original vendor went out of business, the source code is lost, and the binary is stripped. Recently, it has started crashing with segmentation faults, taking down our data pipeline. 

We managed to capture a corpus of payloads. Some of them process fine, while others reliably crash the parser. We need you to investigate the crashes and build a pre-filter in C to protect the legacy parser. 

Your tasks:
1. **Fix the Environment:** The parser currently fails to run at all because it complains about a missing shared library, even though the library is right there in `/app/lib/`. Fix this environment misconfiguration so you can run the binary.
2. **Analyze the Crashes:** Run `/app/legacy_parser <file>` against the files in `/app/corpus/clean/` and `/app/corpus/evil/`. Use core dump analysis (e.g., `gdb`) to trace the intermediate state and figure out exactly what payload structure triggers the segmentation fault.
3. **Build a Pre-Filter:** Write a C program at `/home/user/filter.c` and compile it to `/home/user/filter`. 
    * The program must take a file path as its first CLI argument.
    * It must parse the binary file just enough to determine if it will crash the legacy parser.
    * If the file is "clean" (safe for the parser), your filter must exit with status code `0`.
    * If the file is "evil" (would cause a crash or memory corruption), your filter must exit with status code `1` (or any non-zero value).
    * Do not link your filter to the legacy parser's shared libraries; it must be a standalone C executable.

Please leave the compiled `/home/user/filter` binary ready for our automated integration tests, which will run it against a hidden evaluation corpus of clean and evil payloads. 

Thanks,
IT Operations