You are a release manager preparing a deployment pipeline. You have a Rust-based tool called `release_checker` located at `/home/user/release_manager`. This tool takes a JSON manifest and a previous semantic version string as input, verifies the SHA256 checksum of the manifest's data, and ensures the new version is strictly greater than the previous version.

However, the tool currently fails to compile due to ownership and lifetime issues in `/home/user/release_manager/src/main.rs`. 

Your tasks are as follows:

1. **Fix the Rust Code:**
   Fix the borrow checker and lifetime errors in `/home/user/release_manager/src/main.rs` so that it compiles successfully using `cargo build --release`. The logic must remain functionally the same:
   - Calculate the SHA-256 hash of the `data` field in the manifest and compare it to the `checksum` field (hex string).
   - Compare the semantic versions (Major.Minor.Patch) to ensure the manifest's version is strictly greater than the provided previous version.
   - Print `PASS` to standard output if both checks succeed. Print `FAIL: CHECKSUM` if the checksum is invalid. Print `FAIL: DOWNGRADE` if the version is not strictly greater.

2. **Create Test Fixtures:**
   Create a directory `/home/user/release_manager/fixtures` and populate it with three JSON mock setups. Each JSON file must have the keys: `"version"`, `"data"`, and `"checksum"`.
   - `/home/user/release_manager/fixtures/valid.json`: version `"2.1.0"`, data `"update_package_A"`, checksum `"4027419ef9c2b48cd029fc12d592fba499ffdc7bde0991c28cde3c467a90f1d1"`.
   - `/home/user/release_manager/fixtures/bad_checksum.json`: version `"2.1.0"`, data `"update_package_A"`, checksum `"badbadbadbadbadbadbadbadbadbadbadbadbadbadbadbadbadbadbadbadbadb"`.
   - `/home/user/release_manager/fixtures/downgrade.json`: version `"1.5.0"`, data `"update_package_B"`, checksum `"b80b2a32c25bc5e5108cc9c66af7e20ecba094de193c78d5312010fb09e7de7b"`.

3. **Set up a CI Pipeline Script:**
   Write a bash script at `/home/user/release_manager/ci.sh` that does the following:
   - Compiles the Rust project in release mode.
   - Runs the compiled binary (`./target/release/release_checker`) against the three fixtures in this exact order: `valid.json`, `bad_checksum.json`, `downgrade.json`.
   - For all three runs, use `"2.0.0"` as the previous version argument.
   - Redirects ONLY the standard output of the binary from these three runs into `/home/user/release_manager/ci_results.log`, with one line per run.

Ensure the script is executable and run it to produce the `ci_results.log` file.