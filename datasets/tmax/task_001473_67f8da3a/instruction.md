I am reviewing a Pull Request from a contributor for our Rust-based data processing library, `poly-parser`. The PR attempts to introduce a fast C-based parsing routine to speed up our data ingestion, but the CI is failing. I need you to act as the maintainer, debug the issues, and fix the PR.

The project is located at `/home/user/poly-parser`.

There are three issues with the PR:
1. **Polyglot Build Orchestration:** The contributor added `src/c_src/fast_parse.c` but forgot to configure `build.rs` to actually compile and link this C code. The `cc` crate is already in `Cargo.toml` under `[build-dependencies]`. You must write the correct `build.rs` script to compile `src/c_src/fast_parse.c` into a static library named `fast_parse`.
2. **Memory/FFI Bug:** Once it compiles, `cargo test` will fail. The Rust wrapper in `src/lib.rs` passes a structured data buffer to the C function, but it has a memory-related bug in how it passes the length of the string across the FFI boundary, leading to reading uninitialized memory. Find the bug and fix it so `cargo test` passes consistently.
3. **CI/CD Pipeline Setup:** The contributor deleted our CI config. Recreate a basic GitHub Actions workflow file at `/home/user/poly-parser/.github/workflows/ci.yml` that runs `cargo test` on `ubuntu-latest`.

Once you have fixed the build, fixed the FFI bug, and ensured `cargo test` passes, create a file at `/home/user/review_completed.txt` containing exactly the text: `PR fixed and tested`.