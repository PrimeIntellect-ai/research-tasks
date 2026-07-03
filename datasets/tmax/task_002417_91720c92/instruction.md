You are an engineer tasked with fixing and completing a polyglot Web Application Firewall (WAF) analyzer from scratch. The system uses a high-performance C library for state-machine-based payload parsing (URL decoding), a Rust application that interfaces with the C library via FFI to enforce security policies, and an SQLite database storing the WAF rules. 

Currently, the project in `/home/user/waf_project` is broken in several ways. Your task is to fix the issues, build the system, and run a verification test.

Here are your objectives:

1. **Fix the C Parser (State Machine & Encoding):**
   The file `/home/user/waf_project/c_src/parser.c` implements a basic state machine to URL-decode a string. However, the logic for handling the hex decoding after the `%` character is missing. Implement the missing state machine logic to correctly decode `%XX` hex sequences into their corresponding ASCII characters. 

2. **Fix the Build System (FFI & Linking):**
   There is a script `/home/user/waf_project/build.sh`. It compiles the C code into a shared library `libparser.so`, but the Rust project in `/home/user/waf_project/rust_app` fails to link against it. Fix the build script and/or Rust configuration so that the Rust app successfully compiles and links against `libparser.so`. Ensure that when the Rust binary is executed, it can find the shared library.

3. **Fix the Rust Borrow Checker Issue:**
   The file `/home/user/waf_project/rust_app/src/main.rs` contains a classic Rust borrow checker/lifetime bug involving `CString` and FFI. The code tries to pass a Rust string to the C library, but creates a dangling pointer. Fix this ownership issue so the code compiles safely without warnings or errors.

4. **Schema Migration:**
   The SQLite database `/home/user/waf_project/rules.db` has a single table: `rules (id INTEGER PRIMARY KEY, pattern TEXT)`. Write a bash script `/home/user/waf_project/migrate.sh` that uses the `sqlite3` CLI tool to safely add a new column `action TEXT DEFAULT 'block'` to the `rules` table. Run this migration script.

5. **Execution and Logging:**
   Once built and the database is migrated, run the Rust application via your modified `build.sh` (or a separate run script). The Rust application takes a payload string as an argument. 
   Execute the Rust app with the following exact argument: `"SELECT%20*%20FROM%20users"`
   Redirect the standard output of this execution to `/home/user/waf_project/result.log`.

Criteria for success:
- `result.log` is created and contains the correct output from the Rust program, which should reflect the successfully URL-decoded string.
- The `rules.db` schema includes the new `action` column.
- The project compiles without linking errors or Rust borrow checker errors.