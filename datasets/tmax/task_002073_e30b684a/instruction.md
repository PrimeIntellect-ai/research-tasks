You are an engineer tasked with porting a legacy Linux log-processing tool to a minimal containerized environment. As part of this, we are migrating the core logic to Rust. 

We have partially migrated the code into a Rust workspace located at `/app/vendored/log-processor-1.0.0`. However, the previous developer left it in a broken state. Currently, the project fails to build due to a circular dependency between the internal crates (`semver_parser` and `text_encoder`). Furthermore, the CLI component has not been fully implemented to match the legacy system's exact behavior.

Your tasks are:
1. **Fix the Build (Architecture & Refactoring):** Analyze the `Cargo.toml` files in the `/app/vendored/log-processor-1.0.0` workspace. Refactor the workspace to break the circular dependency between `semver_parser` and `text_encoder`. You may need to create a third internal crate or move traits/structs to resolve it.
2. **Implement the Logic (Data Encoding & Version Comparison):** Complete the implementation of the `cli` crate's main logic. The tool must read lines from `stdin`. Each line will be formatted as `<semver> <raw_text>`. 
   - Parse the semantic version.
   - Encode the `<raw_text>` using a custom Run-Length Encoding (RLE): count consecutive identical characters and append the count to the character (e.g., `aaabbc` becomes `a3b2c1`).
   - Output the formatted strings as `<encoded_text>\t<parsed_semver>` to `stdout`.
   - The output must be sorted in **descending** order based on the semantic version. If versions are equal, sort alphabetically by the encoded text.
3. **Equivalence:** Your compiled binary must be bit-exact in its input/output behavior compared to the stripped legacy binary located at `/app/oracle`. 
4. **CI/CD Pipeline:** Create a GitHub Actions workflow file at `/home/user/repo/.github/workflows/ci.yml` that builds the workspace in release mode and runs `cargo test`. 

Compile your final executable to `/home/user/bin/log-processor` (you will need to create this directory and copy the release binary from the workspace target directory).

Constraints:
- You must use Rust and Cargo.
- Only process valid semantic versions (Major.Minor.Patch). Drop lines with invalid semvers.