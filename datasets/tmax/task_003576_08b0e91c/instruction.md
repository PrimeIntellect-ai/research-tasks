You are an engineer tasked with diagnosing a failing daemon process, fixing its source code, and setting up a lightweight CI/CD deployment pipeline using Git hooks. 

Currently, a custom logging daemon written in C is failing to start. It acts like a system service, but we are running it in user space. The source code is located in a local Git repository at `/home/user/daemon_repo`.

Your objectives are as follows:

1. **Text Processing & Log Analysis**:
   There is a log file from previous crash attempts at `/home/user/old_crash.log`. Use bash text-processing tools (like `grep`, `awk`, or `sed`) to extract ONLY the timestamps (e.g., `2023-10-24T12:00:00Z`) from lines that contain the exact string `[CRITICAL FATAL ERROR]`. Write these extracted timestamps, one per line, to `/home/user/critical_dates.txt`.

2. **Diagnose and Fix the C Daemon**:
   In `/home/user/daemon_repo`, there is a file named `daemon.c`. When compiled and run, the daemon reads a config file at `/home/user/daemon.conf`. Currently, it crashes (segmentation fault) immediately upon starting. 
   Find the bug in `daemon.c` related to file reading/filesystem paths or parsing, and fix it. Commit your fix to the local repository in `/home/user/daemon_repo`. 

3. **Set up a Git Server & CI/CD Hook**:
   - Create a bare Git repository at `/home/user/deploy.git`.
   - Set up a `post-receive` hook in `/home/user/deploy.git/hooks/post-receive`. Ensure it is executable.
   - The hook must act as a deployment CI/CD pipeline. Whenever code is pushed to this bare repository, the hook should:
     a) Checkout the latest code into `/home/user/daemon_build` (create this directory if necessary).
     b) Compile `daemon.c` into an executable named `daemon` using `gcc`.
     c) Execute the compiled `daemon` program in the background (e.g., `./daemon &`).

4. **Deploy**:
   Add the bare repository `/home/user/deploy.git` as a remote named `deploy` in your `/home/user/daemon_repo` repository. Push your fixed `master` branch to the `deploy` remote. If your hook is set up correctly, this will automatically build and start the daemon.

When successful, the daemon will successfully read `/home/user/daemon.conf`, write its PID to `/home/user/daemon.pid`, and write a success message to `/home/user/daemon.log`.

Do not use root privileges. Ensure all paths and filenames exactly match the instructions.