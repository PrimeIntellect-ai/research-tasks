You are tasked with building a minimalist configuration manager that cleans up legacy configuration files and deploys them using a content-addressable storage mechanism via hard links.

You must complete the following phases:

**Phase 1: Legacy Configuration Cleanup**
There is a directory `/home/user/raw_configs` containing 20 legacy configuration files (named `config_01.ini` through `config_20.ini`). 
Using shell utilities (like `sed` or `awk`), transform all these files and save the output to a new directory `/home/user/staged_configs`. 
The transformations required are:
1. Replace any line exactly matching `HOST=localhost` with `HOST=127.0.0.1`.
2. Replace any line exactly matching `DEBUG=true` with `LOG_LEVEL=debug`.
3. Do not modify any other lines.

**Phase 2: Rust Configuration Deployer**
Create a new Rust project named `config_deployer` in `/home/user/config_deployer` (use `cargo new`).
Write a Rust program that does the following when executed:
1. Reads all `.ini` files from `/home/user/staged_configs`.
2. For each file, calculates the length (in bytes) of its contents.
3. Creates a central storage directory at `/home/user/store` (if it doesn't exist) and copies the file there with a new name: `<original_basename>_<size>.ini`. For example, if `config_01.ini` is 150 bytes, it should be copied to `/home/user/store/config_01_150.ini`.
4. Creates a deployment directory at `/home/user/deploy` (if it doesn't exist).
5. Creates a **hard link** in `/home/user/deploy/` pointing to the file in `/home/user/store/`. The hard link must have the original filename (e.g., `/home/user/deploy/config_01.ini` hard-linked to `/home/user/store/config_01_150.ini`).
6. Appends a log entry to `/home/user/deployment_report.log` for each deployed file in the exact following format:
   `LINKED <original_filename> -> store/<stored_filename>`
   (Example: `LINKED config_01.ini -> store/config_01_150.ini`)

**Execution**
- Run your text transformation.
- Build your Rust program using `cargo build --release`.
- Execute the Rust program to perform the deployment.
- Ensure all directories and files mentioned above exist and have the correct contents and link structures.