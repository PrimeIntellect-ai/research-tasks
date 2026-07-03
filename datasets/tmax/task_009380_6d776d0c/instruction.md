You are an IT support technician acting on an escalated ticket from the QA team. 

Ticket #1092: "The log aggregator utility crashes on production payload, but only on recent builds. We attached the crashing payload."

You have been provided a workspace at `/home/user/ticket_1092` containing:
1. `repo/` - A Git repository containing the C++ source code for the log aggregator utility (`aggregator.cpp` and `Makefile`).
2. `attachments/large_payload.txt` - A 10,000-line input file that causes the latest version of the utility to crash with a segmentation fault or abort.

Your objectives are:
1. **Git Forensics & Bisection:** The bug was introduced in a recent commit. The first commit in the repository is known to be good. Use Git bisection (or manual checking) to find the exact commit hash that introduced the crash. 
2. **Test Minimization (Delta Debugging):** The attached `large_payload.txt` is huge. You must use delta debugging techniques (e.g., writing a script to systematically halve the file and test for the crash) to find the absolute minimum combination of lines required to trigger the crash.
3. **Root Cause Analysis:** Read the C++ code of the buggy commit to identify which function causes the crash.

**Deliverables:**
1. Create a minimal reproducible input file at `/home/user/ticket_1092/minimal_payload.txt`. This file must contain the absolute minimum number of lines from `large_payload.txt` necessary to trigger the crash in the buggy build (order of lines must be preserved).
2. Create a JSON report at `/home/user/ticket_1092/report.json` with the following exact keys:
   - `"buggy_commit"`: The full Git commit hash that introduced the bug.
   - `"crashing_function"`: The exact name of the C++ function where the crash/abort originates.

You have full terminal access to write scripts, compile the C++ code (`make` is provided in the repo), and run tests.