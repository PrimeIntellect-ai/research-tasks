I'm a developer trying to fix a failing build for a telemetry validation tool written in Rust. My project is located at `/app/validator`. It relies on a vendored custom decoder package called `fast-decode` located at `/app/fast-decode`.

Right now, I have two major issues:
1. The build in `/app/validator` is failing due to a dependency conflict. I recently updated a serialization library, and now `cargo build` fails because it conflicts with the requirements of the vendored `fast-decode` package. 
2. Even if you fix the build conflict, the decoding logic in `fast-decode` is buggy. It contains an off-by-one error and mishandles corrupted inputs, causing it to either panic or incorrectly accept malformed data. 

Your task is to:
1. Fix the dependency conflict so that `cd /app/validator && cargo build` completes successfully. You may modify the `Cargo.toml` files in both `/app/validator` and `/app/fast-decode` as needed, but keep the core serialization library update intact.
2. Debug and fix the decoding logic in `/app/fast-decode/src/lib.rs`. 
3. Ensure the built binary (`/app/validator/target/debug/validator`) can act as a robust filter. I have provided two directories of test payloads:
   - `/app/corpora/clean/`: Contains valid, well-formed payloads. The validator MUST exit with code `0` for every file in this directory.
   - `/app/corpora/evil/`: Contains malformed payloads designed to trigger the off-by-one error, cause memory allocation panics, or bypass the corrupted input checks. The validator MUST exit with a non-zero code (e.g., `1`) for every file in this directory, without panicking.

The validator binary takes a single file path as its argument: `/app/validator/target/debug/validator <file_path>`.

Please fix the build and the code so that 100% of the clean corpus is accepted and 100% of the evil corpus is rejected gracefully. Do not change the CLI signature of the validator.