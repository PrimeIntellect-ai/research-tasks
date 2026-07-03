You have recently inherited an unfamiliar, legacy C codebase located in `/home/user/legacy_project`. The previous developer left behind a messy build environment that suffers from intermittent failures and unexplained linker errors. 

Your task is to perform a forensic debugging investigation by completing two specific objectives:

**Objective 1: Statistical Anomaly Investigation**
In `/home/user/legacy_project/logs/`, there is a file named `build_history.log`. This file contains the results of the last 10,000 automated build attempts. 
The file is comma-separated with the following columns: `BuildID, Timestamp, EnvFlags, ExitCode`. 
The `EnvFlags` column contains a space-separated list of active feature flags during that build. 
Use Bash tools (awk, grep, sort, etc.) to statistically analyze this log and identify the single environment flag that is perfectly correlated with build failures (`ExitCode` != 0). Note: Builds fail *only* when this specific flag is present.

**Objective 2: Delta Debugging for Linker Errors**
In `/home/user/legacy_project/src/`, there are 100 C source files. When you attempt to compile all of them together (e.g., `gcc -c *.c` works, but linking them fails), you get a compiler/linker error due to a "multiple definition" of a global variable.
You must use delta debugging principles to isolate the exact two files that conflict.
Write a bash script if necessary to minimize the set of files and find the culprit pair. 

**Deliverables:**
Once you have identified the problematic environment flag and the two conflicting source files, create a final report at `/home/user/debug_report.txt` with exactly two lines:
* **Line 1:** The name of the problematic environment flag.
* **Line 2:** The filenames of the two conflicting C files, comma-separated, in alphabetical order (e.g., `module_05.c,module_99.c`).

Ensure your final output precisely matches this format for automated verification.