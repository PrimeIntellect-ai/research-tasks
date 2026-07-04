You are a deployment engineer tasked with setting up a continuous deployment pipeline using Git hooks. The goal is to automatically compile and deploy a C program whenever code is pushed to a centralized repository.

Your task consists of the following phases:

1. **Repository Setup:**
   - Create a bare Git repository at `/home/user/deploy_repo.git`.
   - Create a deployment directory at `/home/user/deploy_target`.
   - Ensure the log file `/home/user/deploy.log` exists (create it if it doesn't).

2. **The C Program (`updater.c`):**
   - Create a local Git repository at `/home/user/source_repo`.
   - In this repository, write a C program named `updater.c`. 
   - The program must accept command-line arguments. If executed with exactly one argument `--deploy`, it must open `/home/user/deploy.log` in append mode and write the exact string: `UPDATER EXECUTED\n`. If called without arguments or with other arguments, it should just exit with code 0.
   - Commit this file to the local repository.

3. **The Git Hook:**
   - Write a `post-receive` hook for the bare repository at `/home/user/deploy_repo.git/hooks/post-receive`. Make sure it is executable.
   - The hook must be a robust Bash script that reads from standard input to get the pushed commit information (format: `oldrev newrev refname`).
   - For every push, the hook must extract the code to a temporary directory.
   - It must attempt to compile `updater.c` into an executable named `updater` using `gcc`.
   - **If compilation succeeds:** 
     - Move the `updater` executable to `/home/user/deploy_target/updater` (overwrite if it exists).
     - Append the exact string `BUILD SUCCESS: <newrev>\n` to `/home/user/deploy.log` (where `<newrev>` is the full hash of the pushed commit).
     - Execute the newly compiled `/home/user/deploy_target/updater` with the argument `--deploy`.
   - **If compilation fails:**
     - Append the exact string `BUILD FAILED: <newrev>\n` to `/home/user/deploy.log`.
     - Exit with a non-zero status.

4. **Triggering the Pipeline:**
   - Add the bare repository as a remote named `origin` to your local repository at `/home/user/source_repo`.
   - Push the `master` branch to `origin` to trigger the hook and deploy the initial version.

Ensure all file paths are absolute and exactly as specified. Do not hardcode commit hashes in your hook, as it must work dynamically for any push.