You are managing configuration states for a deployment system. We need a simple differential backup tool written in Rust that packages only the configuration files that have changed or are new, compared to a base compressed archive.

I have already created a Rust project skeleton for you at `/home/user/config_manager` with the `tar` and `flate2` crates available in `Cargo.toml`. 

Your task is to write the Rust program in `/home/user/config_manager/src/main.rs` that performs the following actions:
1. Opens and reads a base Gzipped Tar archive located at `/home/user/base_config.tar.gz`.
2. Iterates through all the regular files in the directory `/home/user/configs/`.
3. For each file in `/home/user/configs/`, determines if it should be included in an incremental backup. A file should be included if:
   - It does not exist in the base archive.
   - Or, its exact byte content differs from the content of the file with the same name in the base archive.
4. Creates a new Gzipped Tar archive at `/home/user/incremental.tar.gz` containing *only* the new or modified files. The files inside the new archive must not be nested in any subdirectories (i.e., if `/home/user/configs/app.conf` is included, its path in the archive must be exactly `app.conf`).

Note: 
- The files in the base archive also do not have directory prefixes (e.g., they are stored as `app.conf`, not `configs/app.conf`).
- You can assume all configuration files are small enough to be loaded into memory for comparison.
- Once you have written the program, compile and run it to produce `/home/user/incremental.tar.gz`.