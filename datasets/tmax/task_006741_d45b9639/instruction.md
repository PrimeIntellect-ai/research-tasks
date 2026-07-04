You are a platform engineer maintaining the CI/CD pipeline for a web authentication service. A recent architecture update introduced a mandatory session expiration feature to improve web security, but the pipeline is currently failing. 

Your service consists of a C shared library (`libauth.so`) handling core validation logic, and a Rust web service wrapper (`main.rs`) calling it via FFI. 

The build pipeline (`/home/user/pipeline/build.sh`) is broken due to three interconnected issues:
1. **Schema Migration:** The SQLite database `/home/user/pipeline/db.sqlite` is missing the new column for expiration.
2. **ABI / Shared Library Mismatch:** The C library signature in `src/auth.c` hasn't been updated to accept the new expiration parameter.
3. **Memory Safety:** The developer who updated the Rust wrapper introduced a borrow-checker bug related to C-string pointers.

Your task is to fix the pipeline:
1. Migrate the SQLite database (`/home/user/pipeline/db.sqlite`) by adding an `expiry` column (type `INTEGER`) to the `sessions` table.
2. Update the C function `check_auth` in `/home/user/pipeline/src/auth.c`. It currently takes `const char* username` and `const char* token`. Update its ABI to take a third parameter: `int expiry`. The function must simply return `1` if `expiry > 0`, and `0` otherwise.
3. Fix the Rust borrow checker bug in `/home/user/pipeline/src/main.rs`. The code currently drops a `CString` prematurely while extracting a pointer for the FFI call. Fix it so the pointers remain valid during the `check_auth` unsafe call. Do not change the overall logic or the output prints.
4. Execute `/home/user/pipeline/build.sh`. It will compile the C shared library, compile the Rust code, and execute the binary. 

If everything is fixed correctly, the script will execute the compiled application and write "Auth Check: 1" to `/home/user/pipeline/success.log`.