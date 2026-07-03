You are a performance engineer profiling a shell-based task pipeline. Recently, the main job runner script started hanging indefinitely, causing CI pipelines to time out. 

The task pipeline code is located in a Git repository at `/home/user/perf-repo`. 

You know the following:
1. The script `/home/user/perf-repo/runner.sh` executes a recursive function to process tasks.
2. The initial commit (message: "Initial commit") is known to be good and works perfectly.
3. A subsequent commit introduced a bug causing infinite recursion, completely breaking the runner.

Your objectives:
1. Identify the exact commit that introduced the infinite recursion bug.
2. Write the full SHA-1 hash of this bad commit into the file `/home/user/bad_commit.txt`.
3. Fix the bug in `/home/user/perf-repo/runner.sh` on the latest commit (HEAD). You must keep the recursive structure of the `process_jobs` function, but ensure the recursion terminates correctly and processes all three default tasks ("task1", "task2", "task3").

Make sure your fixed script is executable and prints the following output when run without arguments:
Processing task1
Processing task2
Processing task3