You are tasked with resolving a critical concurrency regression in our C-based multithreaded telemetry parser. 

A bug was recently introduced in our repository, causing race conditions that lead to memory corruption and invalid string extraction from system memory dumps. A user submitted a screenshot of the kernel panic and stack trace, but they didn't specify which commit caused it. 

Here is your multi-step mission:

1. **Analyze the Bug Report**: An image artifact is located at `/app/bug_report.png`. Use OCR (e.g., `tesseract`) to read the image. It contains a hidden configuration string and a specific memory offset (formatted like `FATAL_OFFSET:0x...`) that you will need to properly configure the lock boundaries in the code.
2. **Bisect the Regression**: Navigate to the git repository at `/home/user/telemetry_repo`. There are exactly 200 commits. The earlier commits work flawlessly, but a recent commit introduced a race condition in `telemetry.c` and a subtle build configuration failure in the `Makefile`. Use bisection to find the offending commit.
3. **Diagnose and Fix**: Once you identify the bad commit, analyze the concurrency bug (a missing mutex lock around the string extraction buffer). Fix the race condition in `telemetry.c` and resolve the build failure.
4. **Compile the Target**: Your final, fixed C program must be compiled and placed at exactly `/home/user/fixed_parser`. 

**Verification:**
Your compiled executable `/home/user/fixed_parser` will be subjected to rigorous fuzz testing. It must be bit-exact equivalent in its standard output to our reference oracle binary for thousands of randomly generated memory dump strings. The executable should accept a single command-line argument (the memory string) and print the safely extracted output.