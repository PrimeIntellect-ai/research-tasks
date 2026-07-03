You are an engineer tasked with building the security audit phase of a new polyglot build system. You need to create a tool that verifies build artifacts using a custom checksum implementation, migrates legacy audit records, and ties it all together into a build pipeline.

Your task is to implement this system from scratch in `/home/user`.

**Step 1: Test Fixtures & Legacy Data Setup**
Create a bash script at `/home/user/setup_env.sh` that sets up our mock environment:
1. Creates a directory `/home/user/artifacts/`
2. Creates three mock artifact files with the exact contents (no trailing newlines):
   - `/home/user/artifacts/web_ui.tar` containing exactly the string `WEB_UI_MOCK_DATA`
   - `/home/user/artifacts/api_server.bin` containing exactly the string `API_SERVER_MOCK_DATA`
   - `/home/user/artifacts/legacy_db.so` containing exactly the string `LEGACY_DB_MOCK_DATA`
3. Creates a legacy database file at `/home/user/old_registry.txt`. This file represents an old schema that only tracked filenames. It should contain exactly three lines:
   ```
   web_ui.tar
   api_server.bin
   legacy_db.so
   ```

**Step 2: The Rust Audit Tool**
Create a new Rust CLI project at `/home/user/audit-hash`. This tool must perform schema migration and artifact verification.
1. The tool should be invokable via `cargo run -- migrate <legacy_file_path> <artifacts_dir> <output_csv_path>`.
2. **Checksum logic:** You must manually implement the Adler-32 checksum algorithm in Rust to verify the files. Do not use external crates for Adler-32.
   *(Adler-32 reference: Initialize A=1, B=0. For each byte in the input, `A = (A + byte) % 65521` and `B = (B + A) % 65521`. The final checksum is `(B << 16) | A`.)*
3. **Custom Data Structure:** Define a Rust struct `ArtifactRecord` containing the filename (String), the Adler-32 checksum (u32), and a `security_status` (String).
4. **Schema Migration:** When the `migrate` command is run, the tool must:
   - Read the old registry file.
   - For each filename listed, locate the file in the `<artifacts_dir>`.
   - Read the file and compute its Adler-32 checksum.
   - Create an `ArtifactRecord` for each, hardcoding the `security_status` to `VERIFIED`.
   - Write these records to `<output_csv_path>` in a new CSV schema format: `filename,checksum,security_status` (include this header row as the first line).

**Step 3: Build System Orchestration**
Create a build configuration script at `/home/user/build_pipeline.sh`. This script must:
1. Make `setup_env.sh` executable and run it.
2. Compile the Rust project `audit-hash` in release mode.
3. Execute the compiled Rust binary (using the executable in `target/release/`, not `cargo run`) to perform the migration. Pass `/home/user/old_registry.txt` as the legacy file, `/home/user/artifacts/` as the artifacts directory, and `/home/user/registry.csv` as the output CSV.

Ensure that after someone runs `bash /home/user/build_pipeline.sh`, the final `/home/user/registry.csv` file is perfectly formatted and contains the migrated checksums.