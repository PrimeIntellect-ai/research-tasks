You are tasked with fixing a broken polyglot build system in `/home/user/project`.

The project is a C++ application that relies on a Rust static library via FFI and interacts with a SQLite database. Currently, the project fails to build and run due to three distinct issues:

1. **Rust Ownership / Borrow Checker Error**: The Rust library located in `/home/user/project/rust_lib` has a compilation error related to memory management and lifetimes at the FFI boundary. The function `get_system_name` is returning a pointer to a locally dropped `CString`.
2. **Polyglot Build Orchestration**: The `CMakeLists.txt` builds the Rust static library as a custom target, but the `myapp` C++ executable fails to link because it doesn't specify the compiled Rust library (`librust_lib.a`) and standard system libraries (`dl`, `pthread`, `m`) in its `target_link_libraries`.
3. **Schema Migration**: The C++ application expects a specific database schema to run successfully. An initial database exists at `/home/user/project/db.sqlite`, but it is missing a required table update. A migration script is provided at `/home/user/project/schema/migrate.sql`.

Your objective is to:
1. Fix the Rust borrow checker error in `/home/user/project/rust_lib/src/lib.rs` (ensure you don't leak memory, or if you transfer ownership to C++, make sure the C++ side frees it or accept that `into_raw()` is sufficient for this exercise).
2. Fix `/home/user/project/CMakeLists.txt` to correctly link the Rust static library and required system libraries to `myapp`.
3. Apply the SQL migration to `db.sqlite`.
4. Compile the project by creating a `build` directory, running `cmake ..`, and `make`.
5. Run the resulting executable (`./myapp`).

If everything is fixed correctly, the executable will verify the database schema, call the Rust library, and automatically write its success state to `/home/user/project/output.log`.

Do not modify the C++ source files (`src/main.cpp`, `src/wrapper.cpp`); assume they are correct. Ensure the final `output.log` is generated successfully.