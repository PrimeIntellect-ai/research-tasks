You are tasked with fixing a critical reliability issue in our ETL pipeline's configuration manager. 

We have a legacy configuration tracker tool, located at `/app/config_differ` (a stripped ELF binary). It processes pipeline state files that combine JSON metadata with XML-based ETL logic. Recently, we've noticed that certain malformed configuration updates cause the tool to enter an infinite loop, resulting in the generation of massive amounts of duplicate tracking records on retry. 

To prevent this from taking down our infrastructure, we need a high-performance pre-flight filter written in C that can detect these "poisoned" configurations before they are fed to the legacy tracker.

**Your Objectives:**
1. **Analyze the Issue:** We have provided a set of known good configurations in `/app/corpus/clean/` and known bad configurations in `/app/corpus/evil/`. You can also test files against `/app/config_differ` to observe its behavior (it will exit normally on clean files, but output "DUPLICATE_RETRY_ERROR" and crash on evil files).
2. **Determine the Pattern:** Analyze the evil and clean corpora to identify the exact structural anomalies or regex patterns that trigger the failure. The configs use a mix of JSON and XML.
3. **Implement the Filter:** Write a C program at `/home/user/detector.c` and compile it to `/home/user/detector`.
    - The program must accept a single file path as a command-line argument: `/home/user/detector <file_path>`
    - It must be capable of processing large files using stream processing (do not read the entire file into memory at once).
    - It must use standard POSIX regex (`regex.h`) and basic string manipulation to analyze the multi-format contents.
    - If a file is deemed "evil" (contains the poison patterns), the program must print `EVIL` to standard output and exit with status code `1`.
    - If a file is "clean", it must print `CLEAN` to standard output and exit with status code `0`.

**Constraints & Notes:**
- You may use standard bash utilities (`grep`, `awk`, `objdump`, `strings`, etc.) to reverse engineer the binary or analyze the corpora.
- Your final deliverable must be the compiled C binary at `/home/user/detector`.
- An automated test suite will invoke your detector against a hidden evaluation corpus of clean and evil configurations. You must achieve 100% accuracy on both.