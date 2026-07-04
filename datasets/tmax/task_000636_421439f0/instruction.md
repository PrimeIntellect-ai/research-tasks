You are a cloud architect migrating virtualization services to a new automated infrastructure. Part of the migration involves moving a legacy log processing system to a GitOps-based workflow. Currently, an automated background task (similar to a cron job) processes QEMU/VNC startup logs, but it has been failing in the new environment because it writes outputs to unpredictable locations due to environment variables and working directory shifts during background execution.

Your task is to implement a robust, automated processing pipeline triggered by a Git hook.

Here are your specific objectives:

1. **Git Server Setup:**
   - Create a bare Git repository at `/home/user/git_server/migration.git`.
   - Clone this repository locally to `/home/user/migration_workspace`.

2. **C++ Log Parser:**
   - In your local clone (`/home/user/migration_workspace`), write a C++ program named `vnc_parser.cpp`.
   - The C++ program must read from standard input. It will receive lines formatted exactly like this:
     `VM_ID=101 CMD="qemu-system-x86_64 -m 1024 -vnc 192.168.1.50:5901"`
   - The program must parse each line and print the extracted VM_ID and the VNC endpoint in the format: `VM_ID: <ID> | VNC: <IP>:<PORT>`. (e.g., `VM_ID: 101 | VNC: 192.168.1.50:5901`).

3. **Git Hook Configuration:**
   - Create a `post-receive` hook in the bare repository (`/home/user/git_server/migration.git/hooks/post-receive`).
   - The hook must be executable. To enforce strict access control, ensure the hook file has exactly `700` permissions.
   - The hook must do the following when triggered:
     a. Checkout the latest code into a temporary build directory `/home/user/build_env`.
     b. Compile `vnc_parser.cpp` into an executable named `vnc_parser`.
     c. Read the raw log file located at `/home/user/logs/qemu_raw.log`.
     d. Use a text processing pipeline (`grep` and `awk`/`sed`) to filter only lines containing the word `START`, and strip away the timestamp prefix so that only the `VM_ID=... CMD=...` portion is piped into the newly compiled `vnc_parser`.
     e. Save the output of the C++ program to `/home/user/logs/vnc_endpoints.log`.

4. **The "Cron/Background" Anchor Challenge:**
   - Git hooks execute in a restricted, non-interactive environment (similar to cron), often with a different `PATH` and working directory (usually the bare repo). You must ensure your hook uses absolute paths for all input/output files and binaries, or explicitly sets the environment, so the final log is written exactly to `/home/user/logs/vnc_endpoints.log`.

5. **Execution:**
   - The raw log `/home/user/logs/qemu_raw.log` already exists (assume it's populated).
   - Add `vnc_parser.cpp` to the git repository, commit it, and push to the bare repository.
   - The push should trigger the hook, compile the code, process the log, and generate the final output.

Verify your solution by checking the contents of `/home/user/logs/vnc_endpoints.log` after the push.