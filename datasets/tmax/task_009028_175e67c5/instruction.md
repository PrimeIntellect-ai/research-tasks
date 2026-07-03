You are tasked with debugging a multithreaded C++ application that has recently started deadlocking under high contention. A regression was introduced somewhere in the recent commit history of the project's repository.

You have been provided with:
1. A Git repository located at `/home/user/repo` containing the history of the C++ application.
2. A test script located at `/home/user/test.sh` which compiles and runs the application. The script exits with code `0` if the program completes successfully, and exits with code `1` if it detects the deadlock.

Your objectives are:
1. Use `git bisect` (or a manual bisection strategy) utilizing `/home/user/test.sh` to identify the first bad commit that introduced the deadlock. The known good commit is the very first commit in the repository (`HEAD~49`), and the known bad commit is the latest (`HEAD`).
2. Once you have identified the first bad commit, check it out and run `/home/user/test.sh` manually. This will generate a mock memory dump file named `crash.dmp` in the repository root (`/home/user/repo/crash.dmp`).
3. Analyze this binary memory dump using standard shell tools (e.g., `strings`) to extract the exact deadlock thread signature. The signature you are looking for is a string in the format `DEADLOCK_THREAD_ID=<hex_value>`.
4. Create a file at `/home/user/solution.txt` containing exactly one line with the short commit hash (first 7 characters) of the first bad commit and the extracted hex value, formatted as follows:
   `COMMIT:<short_hash>,ID:<hex_value>`

Example of expected format in `/home/user/solution.txt`:
`COMMIT:a1b2c3d,ID:0x1A2B3C`