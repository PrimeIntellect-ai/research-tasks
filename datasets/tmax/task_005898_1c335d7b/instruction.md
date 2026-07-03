You are a backup operator testing a simulated staged restoration deployment process. You need to create a deployment pipeline using a local Git server, git hooks, and a custom C program to simulate restoring files to a target directory.

Please perform the following tasks:

1. **Environment Setup**:
   - Append `export BACKUP_ENV_ACTIVE=1` to the file `/home/user/.bashrc`.

2. **Git Server and Staging Setup**:
   - Initialize a bare Git repository at `/home/user/restore_deploy.git`.
   - Create a staging directory at `/home/user/deploy_staging`.
   - Create a `post-receive` hook in the bare repository (`/home/user/restore_deploy.git/hooks/post-receive`). The hook must be executable and do the following:
     - Check out the pushed files to the work tree at `/home/user/deploy_staging`.
     - Compile the file `restore_sim.c` (which will be pushed) into an executable named `restore_bin` inside the staging directory.
     - Execute the compiled `restore_bin` from within `/home/user/deploy_staging`. While executing it, provide the environment variable `RESTORE_DIR=/home/user/production_restore`.

3. **C Program and Workspace Configuration**:
   - Create a workspace directory at `/home/user/workspace` and initialize it as a local Git repository.
   - Add the bare repository as a remote named `origin`.
   - Inside the workspace, create a file named `backup_index.txt` containing exactly two lines:
     `data1.bin`
     `data2.bin`
   - Write a C program in the workspace named `restore_sim.c`. This program must:
     - Read the `RESTORE_DIR` environment variable. If it is not set, the program should exit with code 1.
     - Create the directory specified by `RESTORE_DIR` with `0755` permissions (if it does not already exist).
     - Open and read the `backup_index.txt` file from the current working directory.
     - For each line in `backup_index.txt` (which represents a filename, stripping any trailing newline), create that file inside the directory specified by `RESTORE_DIR`.
     - Write the exact string `RESTORED_SUCCESS\n` into each of these created files.
     - Close all files and exit cleanly.

4. **Deployment**:
   - Commit `backup_index.txt` and `restore_sim.c` to your workspace repository (use the `master` branch).
   - Push the commit to the `origin` remote to trigger the `post-receive` hook.

If done correctly, pushing to the bare repository will automatically compile the C code and generate the restored files in `/home/user/production_restore`.