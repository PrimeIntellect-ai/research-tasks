You are tasked with fixing a multi-file Rust project that fails to compile. 

We are migrating a data processing pipeline from Python to Rust. The project is located in `/home/user/pipeline_proj`. 
Currently, the Rust application fails to compile due to ownership and type issues introduced during a naive translation from Python. 

Here is what you need to do:
1. **Fix the compilation error**: Look at `/home/user/pipeline_proj/src/transformer.rs`. It was translated from the Python reference file `/home/user/pipeline_proj/reference.py`. The Rust version fails to compile because it attempts to return references to locally created `String`s (a classic borrow checker error). Fix `transformer.rs` and update `/home/user/pipeline_proj/src/main.rs` if necessary so that the project compiles and functionally matches the Python reference.
2. **Fix the E2E Test Orchestrator**: We have an end-to-end test script at `/home/user/pipeline_proj/e2e_test.sh`. It is supposed to:
   - Compile the Rust project for release.
   - Run the data generator `/home/user/pipeline_proj/generate_data.py` to produce standard output.
   - Pipe the generator's output into the compiled Rust binary (`target/release/pipeline_proj`).
   - Check if the output exactly matches the expected transformed output (which should be a list of uppercase names of active users, each on a new line).
   - Write exactly the string `SUCCESS` to `/home/user/test_results.log` if the output matches, or `FAILURE` otherwise.
   Currently, the script is incomplete and buggy. Fix the bash script so it performs these steps correctly.

3. **Run the tests**: Execute `/home/user/pipeline_proj/e2e_test.sh` so that `/home/user/test_results.log` is created.

**Requirements**:
- Do not change the logic of the transformation; it must match `reference.py`.
- Ensure `/home/user/test_results.log` contains exactly `SUCCESS` (with a trailing newline) after running the fixed script.
- Standard CLI tools and the Rust `cargo` toolchain are available.