You are managing a configuration pipeline where system state changes are recorded as Write-Ahead Logs (WAL) and periodically archived. Due to a race condition and potential log injection vulnerabilities, some WAL files are being corrupted or injected with malicious commands.

There are two main objectives:

1. **Write a Rust Sanitizer**: 
   Create a Rust CLI utility in `/home/user/wal_check` (you must initialize the Cargo project yourself). 
   The utility must take exactly one argument: the path to a WAL file.
   It should exit with `0` if the WAL file is perfectly "clean", and `1` (or any non-zero) if it is "evil" (corrupted/malicious).
   
   A WAL file is "clean" if and only if:
   - The first line is exactly `WAL_START`
   - The last line is exactly `WAL_END`
   - It contains absolutely NO lines featuring the substring `../` (path traversal attempt)
   - It contains absolutely NO lines featuring the substring `EXEC=` (malicious execution attempt)

   Build your project in release mode: `cargo build --release`. The executable should be at `/home/user/wal_check/target/release/wal_check`.

2. **Fix the Processing Pipeline**:
   The system runs two local services configured in `/home/user/services/`:
   - `producer.py` (simulates the system writing WALs to `/home/user/run/spool/pending/`)
   - `archiver.sh` (periodically tars up pending files and moves them to `/home/user/run/spool/processed/`)
   
   Currently, `archiver.sh` just blindly tars everything. Edit `/home/user/services/archiver.sh` so that it uses your `wal_check` tool to inspect each `.wal` file in `/home/user/run/spool/pending/` BEFORE archiving. 
   - Only "clean" files should be included in the tarball.
   - "Evil" files should be deleted.
   - You must also generate a `manifest.sha256` file containing the SHA-256 checksums of the clean files *before* they are added to the archive, and include this manifest inside the tarball at the root.

Ensure both services are running and that a successful end-to-end flow is achieved. The producer creates files every 2 seconds. The archiver runs in a loop.