Our CI/CD pipeline for our internal web security dashboard is currently blocked. We have an old, unmaintained binary dependency at `/app/legacy_auth_gen` that was historically used to generate secure validation tokens. It is crashing on our new runners, and we need to replace it entirely with a robust, memory-safe C microservice.

Your task is to build this replacement and integrate it.

Here is what you need to do:

1. **Analyze the Legacy Binary:** 
   The stripped binary `/app/legacy_auth_gen` takes a single 32-bit unsigned integer as a command-line argument and prints a transformed 32-bit unsigned integer to standard output. Analyze its behavior (via black-box testing, `objdump`, or `gdb`) to deduce the exact numerical algorithm it uses to transform the input into the output.

2. **Implement the Replacement Service (C):**
   Write a C program at `/home/user/auth_service.c` and compile it to `/home/user/auth_service`. 
   This service must:
   - Listen on TCP port `9090` on `127.0.0.1`.
   - Accept incoming TCP connections.
   - Expect requests in the exact format: `GENERATE <number> AUTH <secret>\n`
   - Validate the `<secret>`. The accepted secret must be exactly `ci_cd_pipe_88`.
   - If the secret is correct, run the deduced numerical algorithm on `<number>` and return `SUCCESS <transformed_number>\n`.
   - If the secret is incorrect or the format is wrong, return `ERROR\n` and close the connection.
   - Run cleanly without memory leaks.

3. **Schema Migration:**
   The legacy tool logged its activity to an SQLite database at `/app/metrics_legacy.db` using the schema:
   `CREATE TABLE logs (id INTEGER PRIMARY KEY, input_val INTEGER, timestamp TEXT);`
   
   We need to migrate this to a new schema at `/home/user/metrics_v2.db`. Write a script or C code to migrate all existing rows from `/app/metrics_legacy.db` to `/home/user/metrics_v2.db` with the new schema:
   `CREATE TABLE auth_logs (log_id INTEGER PRIMARY KEY, requested_val INTEGER, generated_val INTEGER, migration_date TEXT);`
   * Requirement: `generated_val` must be computed using your new C algorithm for each migrated row. `migration_date` should just be "2023-10-01" for all migrated rows.

Once you have written and compiled the C server, start it in the background so it is listening on port 9090. Ensure `/home/user/metrics_v2.db` is successfully created and populated.