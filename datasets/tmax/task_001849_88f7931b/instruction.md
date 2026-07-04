You are a developer tasked with organizing a small polyglot data processing pipeline. We are migrating an old data format to a new JSON-based schema.

Currently, there is a C source file located at `/home/user/schema_gen.c`. This program, when compiled and executed, outputs a legacy user database to standard output. The output is Base64 encoded. Once decoded, the data is in a pipe-separated (`|`) format with the following header:
`USER_ID|USER_NAME|CREATED_AT`

Your task is to orchestrate the build and migration process by doing the following:

1. Write a script (in any language of your choice) that reads a file containing this Base64 encoded string, decodes it, and performs a schema migration to a standard JSON array of objects.
2. The schema migration must apply the following transformations to each record:
   - `USER_ID` becomes `id` (must be represented as an integer).
   - `USER_NAME` becomes `username` (string).
   - `CREATED_AT` becomes `joined_date` (string).
   - Add a new boolean field `active` set to `true` for all records.
3. Create a `Makefile` at `/home/user/Makefile` with a default `all` target that orchestrates the entire pipeline:
   - Compiles `/home/user/schema_gen.c` into an executable named `schema_gen` in `/home/user/`.
   - Runs `schema_gen` and saves its Base64 output to `/home/user/legacy.b64`.
   - Executes your script to read `/home/user/legacy.b64` and output the migrated JSON array to `/home/user/migrated_schema.json`.

Make sure you write your script and the Makefile to `/home/user/`, and then run `make` so the final output file `/home/user/migrated_schema.json` is generated. The JSON must be a valid JSON array of objects.