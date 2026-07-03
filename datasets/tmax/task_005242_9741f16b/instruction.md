You are a web developer working on a backend feature to migrate a legacy file tracking system for user avatars to a new microservice. 

The legacy database export is located at `/home/user/app/legacy.csv`. It has two columns: `user_id` and `filepath`. 
The target schema for the new microservice must be a JSONL (JSON Lines) file named `/home/user/app/new_schema.jsonl` where each line is a JSON object in the format:
`{"user_id": "1", "avatar_hash": 123}`

Before the files can be migrated and hashed, two things need to happen:
1. **Polyglot Processing Step:** A legacy C utility modifies the files slightly before they are stored. The source code is at `/home/user/app/hasher.c`. You must compile this file into an executable named `/home/user/app/hasher`. This utility reads from standard input and writes to standard output.
2. **Algorithmic Checksum Translation:** We have a prototype checksum algorithm written in Python at `/home/user/app/checksum.py`. Because the target container image for the migration script does not include Python to save space, you must translate this exact logic into pure Bash (or use standard Unix utilities like `awk`, `od`, `head` within Bash). 

**Your Task:**
Write and execute a Bash script at `/home/user/app/migrate.sh` that does the following:
1. Compiles `/home/user/app/hasher.c` to `/home/user/app/hasher` using `gcc`.
2. Reads `/home/user/app/legacy.csv` (skipping the header).
3. For each file referenced in the CSV:
   a. Pipes the file contents through the compiled `./hasher` executable.
   b. Computes the custom checksum of the **modified** contents using your translated Bash logic (recreating the logic found in `checksum.py`).
   c. Appends the result to `/home/user/app/new_schema.jsonl` in the required JSON schema.

Everything should be handled in `/home/user/app/migrate.sh` so that running `bash /home/user/app/migrate.sh` generates the complete `/home/user/app/new_schema.jsonl` file.