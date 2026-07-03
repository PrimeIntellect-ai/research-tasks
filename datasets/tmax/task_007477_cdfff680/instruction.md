You are a cloud architect managing a migration of a legacy filesystem service to a new staged deployment environment. To ensure a safe, staged rollout, you need to develop a custom C utility that performs connectivity diagnostics, backs up the current configuration and data, and deploys it to the staging directory.

Your task has several phases:

1. **Dependency and Environment Prep**: 
You have a configuration file located at `/home/user/migration.conf` (which already exists). 
First, start a temporary local python HTTP server on the port specified in the config file (`CHECK_PORT`) in the background. This simulates the readiness of the staged deployment endpoint.

2. **C Utility Development**:
Write a C program at `/home/user/migrator.c` that performs the following actions:
- **Configuration Parsing**: Read `/home/user/migration.conf`. This file has the format `KEY=VALUE` on each line. You must extract `SOURCE_DIR`, `BACKUP_DIR`, `STAGE_DIR`, and `CHECK_PORT`.
- **Connectivity Diagnostic**: Create a TCP socket and attempt to connect to `127.0.0.1` on the extracted `CHECK_PORT`. If the connection fails, the program must write `{"status": "failed", "reason": "connectivity"}` to `/home/user/migration.log` and exit with code 1.
- **Backup Strategy**: If the connection succeeds, use the `system()` function to create a gzipped tarball of the contents of `SOURCE_DIR`. Save this archive as `archive.tar.gz` inside the `BACKUP_DIR`.
- **Staged Restore/Deployment**: Extract the contents of `archive.tar.gz` into `STAGE_DIR` using `system()` and the `tar` command.
- **Verification Logging**: After a successful deployment, append the exact string `{"status": "success", "phase": "staged"}` to `/home/user/migration.log` with a trailing newline.

3. **Compilation and Execution**:
- Compile your C code to an executable named `/home/user/migrator` using `gcc`.
- Run the executable. 

If everything is correct, the staging directory will contain a copy of the source data, the backup directory will contain the tarball, and the log file will reflect a successful staged deployment.