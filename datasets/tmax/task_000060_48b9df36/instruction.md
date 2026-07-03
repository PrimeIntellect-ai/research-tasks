You are a platform engineer responsible for building a new local CI/CD testing step. We are moving away from our old testing tool and you need to write a Bash script that reliably builds our polyglot application, executes a database schema migration, and runs a core integration test.

Our application components are currently located in `/home/user/src/`. It consists of a core C library (`libcompute.c`) and a C++ executable (`main.cpp`) that dynamically links to this C library and reads from a SQLite database. 

Your task is to write an executable Bash script at `/home/user/ci_test.sh` that strictly performs the following steps when executed:

1. **Polyglot Build & Linking:**
   - Compile `/home/user/src/libcompute.c` into a dynamically linked shared library named `libcompute.so` located in the `/home/user/build/` directory.
   - Compile the C++ program `/home/user/src/main.cpp` into an executable named `app` located in `/home/user/build/`.
   - The C++ program requires linking against the new `libcompute.so` library as well as the standard `sqlite3` library. 

2. **Database Setup & Schema Migration:**
   - Initialize a new SQLite database at `/home/user/build/app.db` by executing the SQL schema found in `/home/user/src/schema_v1.sql`.
   - Apply the database migration script located at `/home/user/src/migration_v2.sql` to update the `app.db` schema.

3. **Execution & Verification:**
   - Run the compiled `app` executable, passing the path to the SQLite database (`/home/user/build/app.db`) as its first and only argument.
   - Since `app` depends on `libcompute.so`, ensure your script configures the environment (e.g., library paths) so the dynamic linker can find the shared library during runtime.
   - Capture standard output of the `app` execution and redirect it precisely to `/home/user/test_result.log`.

Make sure your script creates the `/home/user/build/` directory if it does not exist, and ensure `/home/user/ci_test.sh` is given execute permissions. 

Your task is complete once `/home/user/ci_test.sh` is fully written and executable. An automated system will run your script and verify the contents of `/home/user/test_result.log`.