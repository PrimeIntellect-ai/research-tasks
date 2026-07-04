You are a Site Reliability Engineer (SRE). We have a proprietary daemon, located at `/home/user/uptime_agent`, that monitors our service uptime. Recently, it has been crashing intermittently in production with segmentation faults or double-free aborts. We do not have the source code for this binary.

Your task is to:
1. Reverse engineer the `/home/user/uptime_agent` binary to understand the concurrency model. Identify the two thread entry-point functions that are causing the race condition over a shared global pointer.
2. Create a Minimal Reproducible Example (MRE) in `/home/user/mre.c` that mimics the exact bug. It must define the shared global pointer, the two thread functions with the same names as in the binary, and a `main` function that spawns both threads in a loop to forcefully trigger the race condition.
3. Create a patched version in `/home/user/patched.c`. This file must fix the race condition from your MRE by introducing a global `pthread_mutex_t` named `uptime_mutex`. Ensure that the mutex is properly locked and unlocked around the critical sections in both thread functions.
4. Create a text file `/home/user/bug_report.txt` containing exactly the names of the two thread functions, one per line.

Ensure that `/home/user/mre.c` and `/home/user/patched.c` can be compiled with `gcc -pthread`. Do not use any external libraries other than standard C libraries and pthreads.