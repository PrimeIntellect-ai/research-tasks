You are the on-call engineer and have been paged at 3:00 AM. The company's critical data preprocessing pipeline has completely halted after a botched hotfix deployed by a junior developer before they went on vacation.

The pipeline processes daily data dumps, but currently suffers from multiple cascading failures.

Your investigation starting point is the git repository located at `/home/user/data_pipeline` and the incoming data directory at `/home/user/incoming_data/`.

Here is the situation:
1. **The Shell Script is Broken:** The script `/home/user/data_pipeline/process_all.sh` is supposed to iterate over all files in `/home/user/incoming_data/` and pass them to the Rust binary. However, it fails completely on filenames with spaces (which recently started appearing in the incoming data).
2. **Compilation Failure:** The Rust binary `data_parser` inside the repository fails to compile. The latest commit introduced a linker/compiler error related to dependencies.
3. **Infinite Recursion:** Once compiled, the Rust program crashes with a stack overflow (infinite recursion) when parsing the nested file format found in the incoming data. You need to fix the logic in `src/main.rs`.
4. **Missing Secret:** The Rust program requires an API token to stamp the output. The token was accidentally removed from the codebase in a previous commit and is now missing. The current code expects the token to be read from a file located at `/home/user/secret.txt`. You must dig into the Git history of the repository to find the hardcoded API token, and write it into `/home/user/secret.txt`.

**Your Objectives:**
1. Fix `/home/user/data_pipeline/process_all.sh` so it correctly handles filenames with spaces.
2. Fix the compilation errors in the Rust project in `/home/user/data_pipeline/`.
3. Fix the infinite recursion bug in `src/main.rs`. The parser is supposed to strip `[NODE: ` and the trailing `]` but it gets stuck in a loop if it doesn't slice the string correctly.
4. Recover the lost API token from the git history and save it to `/home/user/secret.txt`.
5. Run the fixed `/home/user/data_pipeline/process_all.sh` script.

**Verification:**
The script, when run successfully, will cause the Rust program to append to `/home/user/output.log`.
The automated tests will verify:
- `/home/user/secret.txt` contains exactly the recovered API token.
- `/home/user/output.log` contains the successfully parsed outputs for all files in the incoming directory.