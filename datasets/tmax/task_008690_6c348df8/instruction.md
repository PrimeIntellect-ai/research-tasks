You are acting as a Linux systems engineer responsible for hardening configurations and managing a staged rollout of an auditing tool. 

You need to complete two main objectives: fix a C++ auditing binary so it enforces strict file permissions, and write an idempotent deployment script to roll it out across environments.

**Part 1: C++ Binary Hardening**
You have a skeleton file at `/home/user/src/audit_processor.cpp`. 
1. Modify this C++ program to accept exactly one command-line argument (a path to a configuration file).
2. The program must use the `stat` system call to check the file permissions of the given path.
3. If the file permissions are exactly `0600` (`-rw-------`), the program must print "SECURE" to standard output and exit with code 0.
4. If the file permissions are anything else, it must print "INSECURE" and exit with code 1.
5. If the file does not exist or the wrong number of arguments is provided, print an error and exit with code 1.
6. Compile the code using `g++` to produce an executable at `/home/user/src/audit_processor`.

**Part 2: Idempotent Staged Deployment**
Write a shell script at `/home/user/deploy.sh` that performs a rolling deployment of the compiled binary. The script must be fully idempotent (safe to run multiple times without causing errors or duplicate data) and perform the following:
1. Create the environment directories if they do not exist: `/home/user/deploy/staging`, `/home/user/deploy/prod_a`, and `/home/user/deploy/prod_b`.
2. Copy the `audit_processor` binary to the `staging` directory and enforce read/execute permissions for the owner only (`0500`).
3. Create a configuration file at `/home/user/deploy/staging/config.txt` containing the text `v1`. Enforce strict read/write permissions for the owner only (`0600`).
4. Execute the staging binary against the staging config file: `/home/user/deploy/staging/audit_processor /home/user/deploy/staging/config.txt`.
5. Check the output of the binary. If it outputs exactly `SECURE`:
    a. Roll out the binary to `prod_a` and `prod_b` with the same `0500` permissions.
    b. Create `config.txt` (containing `v1`) with `0600` permissions in both prod directories.
    c. Write a final log file at `/home/user/deploy.log` containing exactly these two lines:
       ```
       Staging: SUCCESS
       Prod: SUCCESS
       ```
    Note: `/home/user/deploy.log` must be overwritten, not appended, so that multiple runs of `deploy.sh` yield the same exact file contents.

Please implement the C++ code, compile it, write the deployment script, and finally run `/home/user/deploy.sh` to complete the task.