You are an engineer scaffolding the end-to-end testing orchestrator for a new polyglot build system. 

Your task is to write a single Bash script at `/home/user/orchestrate.sh` (ensure it is executable) that performs a schema migration, enforces environment constraints, and orchestrates a mock end-to-end test run.

The script must perform the following sequence of operations:

1. **Constraint Satisfaction**:
   - The test suite restricts CPU usage. Your script must check the `MAX_CORES` environment variable.
   - If `MAX_CORES` is not set, set it to `2` for the remainder of the script's execution.
   - If `MAX_CORES` is set to `4` or higher, your script must immediately exit with status code `1`.

2. **Schema Migration**:
   - Our mock application uses a flat-file database. Read the initial database file located at `/home/user/v1.db`.
   - The v1 schema is a headerless CSV with the format: `id,name,role`
   - Transform the data into the v2 schema, which has the format: `id,role,name,is_active`
   - Set the `is_active` field to the literal string `true` for all records.
   - Save the transformed data to `/home/user/v2.db`.

3. **End-to-End Test Orchestration**:
   - Execute the existing test binary at `/home/user/bin/e2e_tester`, passing the newly migrated database as its first positional argument (i.e., `/home/user/v2.db`).
   - Redirect the standard output of the `e2e_tester` command to `/home/user/test.log`.
   - Finally, append the literal string `SUCCESS` on a new line to `/home/user/test.log` if the `e2e_tester` command returns an exit code of `0`. If it returns a non-zero exit code, append `FAILURE`.

Ensure your script runs cleanly and produces the exact output formats requested. Run your script after creating it to fulfill the final state requirements.