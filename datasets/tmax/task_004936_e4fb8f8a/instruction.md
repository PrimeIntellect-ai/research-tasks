You are a developer debugging a failing build for a mathematical expression processor. 

In `/home/user/project`, there is a build script `build.sh` that compiles a C++ code generator and then uses it to process a large corpus of fuzzed mathematical formulas (`fuzz_corpus.txt`). 

Currently, `build.sh` fails. Your objectives are:

1. **Fix the build environment misconfiguration**: The script compiles the tool but fails to execute it correctly due to a missing environment variable required for dynamic linking to local libraries. You must modify `build.sh` so that the `generator` executable successfully finds its required shared library located in `./libmath`.
2. **Delta Debugging**: Even after the environment is fixed, the build script will fail because the C++ `generator` program crashes (Segmentation fault) on one specific line in `fuzz_corpus.txt`. The corpus contains base64-encoded strings. You must isolate exactly which line causes the crash.
3. **Serialization Recovery**: Decode the base64 payload of the crashing line to reveal the underlying plaintext string that triggers the bug.

**Required Outputs:**
Once you have identified the issue, create the following files:
*   `/home/user/line_number.txt`: Must contain only the 1-based line number of `fuzz_corpus.txt` that causes the crash.
*   `/home/user/bug_report.txt`: Must contain the exact, decoded plaintext string from that line.

Do not modify the C++ source code itself; your job is to fix the build script's environment setup and isolate the bad input.