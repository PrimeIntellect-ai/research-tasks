You are tasked with fixing a buggy rate-limiting algorithm written in Rust, translating it into a Bash script to organize project files, and writing a test suite for it.

Currently, in `/home/user/project`, there is a conceptual rate-limiting algorithm in `/home/user/project/limiter_logic.rs`. This script is meant to take a list of incoming "request" files and organize them into queue directories (acting as a token bucket with a maximum capacity of 5 files per queue). However, it currently contains a classic Rust ownership/borrow checker bug. 

Your tasks are:

1. **Rust Debugging:** Identify the ownership bug in `/home/user/project/limiter_logic.rs`. Create a file at `/home/user/project/rust_bug.txt` containing exactly one sentence explaining the fix (e.g., "The variable X needs to be cloned before being moved into the loop."). You do not need a Rust compiler to find this; analyze the source text.

2. **Code Translation & Validation:** Translate the fixed logic into a pure Bash script at `/home/user/project/organizer.sh`. The script must:
   - Accept a source directory as its first argument.
   - Read all regular files in that directory.
   - Move them into `/home/user/project/queues/queue_X/` directories, where `X` starts at 1 and increments.
   - Enforce the "rate limit": No `queue_X` directory may contain more than 5 files. Once `queue_1` has 5 files, the script must start moving files to `queue_2`, and so on.
   - Sort the files alphabetically before moving them to ensure deterministic behavior.
   - Ensure the script is executable (`chmod +x`).

3. **Unit Testing:** Write a Bash test script at `/home/user/project/test_organizer.sh` that:
   - Creates a temporary directory with 12 empty files named `req_01.txt` through `req_12.txt`.
   - Clears any existing directories in `/home/user/project/queues/`.
   - Runs `./organizer.sh` on the temporary directory.
   - Verifies that `queue_1` has exactly 5 files, `queue_2` has exactly 5 files, and `queue_3` has exactly 2 files.
   - Exits with code 0 if all assertions pass, and >0 if any fail.
   - Ensure the test script is executable.

Use only bash built-ins, coreutils, and standard CLI tools.