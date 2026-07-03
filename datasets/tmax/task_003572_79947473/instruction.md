You are a DevOps engineer tasked with debugging a log aggregation system. 

We have a Go script located at `/home/user/log_processor.go` that reads all log files in the `/home/user/logs/` directory to calculate usage metrics. However, the system has started hanging indefinitely during the execution of this script, preventing logs from being processed.

Your task is to diagnose and fix the issue using the following steps:

1. **Diagnose**: Investigate why the script hangs. You may find system call tracing tools (like `strace`) highly effective for identifying where and why the program is blocking.
2. **Identify**: Determine the exact absolute path of the specific file causing the system to hang. Write this absolute path into a file named `/home/user/problem_file.txt`.
3. **Reproduce**: Create a minimal reproducible example script at `/home/user/repro.go`. This Go program should take a single file path as a command-line argument and demonstrate the exact same hanging behavior when run against the problematic file.
4. **Fix**: Modify `/home/user/log_processor.go` so that it robustly skips any file in the directory that is not a standard, regular file (e.g., it should ignore directories, symlinks, pipes, sockets, etc.). 
5. **Execute**: Run your patched `/home/user/log_processor.go`. Redirect its standard output to `/home/user/output.log`.

Ensure that:
- `/home/user/problem_file.txt` contains exactly one line with the absolute path.
- `/home/user/repro.go` compiles and successfully reproduces the blocking bug when tested on the bad file.
- `/home/user/log_processor.go` finishes execution gracefully without hanging, and `/home/user/output.log` is generated successfully.