You have just inherited a C codebase for a multithreaded job queue, located at `/home/user/job_queue`. 

Recently, the team noticed that under certain workloads, the application hangs entirely. Threads seem to deadlock, and CPU usage on one thread spikes to 100%. 

You know the following:
1. The bug was introduced somewhere in the recent Git history. The initial commit (tagged `v1.0`) is known to be good. The current `main` branch `HEAD` is bad.
2. A test script `/home/user/job_queue/test.sh` is provided. If the code is working, it will compile the program, run a threaded workload, and exit successfully within a second. If the code has the regression, the script will hang and eventually timeout (exiting with a non-zero status).

Your tasks are:
1. Find the exact commit that introduced this regression. Write the full 40-character Git commit hash to `/home/user/bug_commit.txt`.
2. Analyze the code in the buggy commit to understand the root cause. You will find that an off-by-one boundary error in a loop condition causes an infinite loop while holding a critical mutex, resulting in the apparent "deadlock" for all other threads.
3. Fix the bug in the `queue.c` file on the current `main` branch. 
4. Ensure that `./test.sh` runs and exits successfully with code `0`.

Please complete these steps using standard Linux terminal commands, Git, and your preferred command-line text editor.