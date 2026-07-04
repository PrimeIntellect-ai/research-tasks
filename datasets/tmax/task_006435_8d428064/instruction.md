You are an infrastructure engineer working on a local build automation pipeline for a custom C++ provisioning tool. 

Please complete the following tasks:

1. Write a C++ program at `/home/user/provisioner.cpp`. 
   - The program must read the environment variable `PROVISION_TARGET_DIR`.
   - If the environment variable is not set or is empty, the program must exit with a non-zero exit code (e.g., return 1).
   - If the environment variable is set, the program must create a file named `status.txt` inside the directory specified by the environment variable.
   - The file `status.txt` must contain exactly the string `SUCCESS` (followed by a newline).
   - The program should exit with code 0 on success.

2. Write a bash build script at `/home/user/ci_pipeline.sh` that performs the following steps in order:
   - Compiles `/home/user/provisioner.cpp` into an executable named `/home/user/provisioner` using `g++`.
   - Creates a directory `/home/user/target_env` if it doesn't already exist.
   - Sets and exports the environment variable `PROVISION_TARGET_DIR=/home/user/target_env`.
   - Executes the compiled `/home/user/provisioner` binary.
   - Creates a compressed tarball archive at `/home/user/release.tar.gz` containing only the `/home/user/provisioner` executable (do not include the directory structure, just the file).
   - Make sure the script is executable.

3. Configure the user's environment by appending the line `export PROVISION_ENV_MODE=production` to the end of `/home/user/.bashrc`.

4. Finally, execute `/home/user/ci_pipeline.sh` so that all the artifacts are generated and the `status.txt` file is created.