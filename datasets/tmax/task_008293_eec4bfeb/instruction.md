You are a QA engineer tasked with setting up a cross-language testing environment for a new URL routing component. The project consists of a Rust-based routing CLI and a Python test harness. Currently, the environment is broken: the Rust code fails to compile due to lifetime issues in its custom data structures, the Python test harness needs a patch applied, and there is no unified build orchestration.

Your objectives:

1. **Fix the Rust Router**:
   Navigate to `/home/user/qa_env/rust_router/`. The file `src/main.rs` contains a custom data structure `RouteMatch` and an `extract_params` function designed to parse URL routing parameters (e.g., extracting `id` from `/users/:id` given the path `/users/123`). 
   However, the code currently fails to compile because the lifetimes of the pattern string slices and the path string slices are tangled improperly in the struct and function signatures. Refactor `RouteMatch` and the `extract_params` signature so that the struct correctly holds references to both the pattern keys and the path values without allocating new `String`s (i.e., fix the lifetimes). Do not change the standard output format of the Rust program.

2. **Patch the Python Test Harness**:
   In `/home/user/qa_env/test_env/`, there is a `test_runner.py` script. Apply the patch file located at `/home/user/qa_env/update.patch` to this script. The patch introduces logic to parse `routes.json` and feed structured data into the Rust CLI.

3. **Orchestrate the Build**:
   Create a `Makefile` in `/home/user/qa_env/` with a default `all` target that:
   - Compiles the Rust project (using `cargo build` in the `rust_router` directory).
   - Runs the patched Python script (`python3 test_env/test_runner.py`).

4. **Run the Tests**:
   Execute your `Makefile`. The Python script will test the Rust binary and generate a log file at `/home/user/qa_env/test_results.log`. 

Ensure that `/home/user/qa_env/test_results.log` is successfully created and populated with the test results.