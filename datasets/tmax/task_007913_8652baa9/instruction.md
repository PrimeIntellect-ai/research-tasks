You are acting as a Build Engineer. We are upgrading our CI/CD artifact management tools. We currently have a Python script that takes legacy artifact metadata, migrates the schema to v2, merges multiple artifact lists, and sorts them. 

The Python script is slow on massive artifact lists, so we need to translate it into Go and verify its correctness and performance.

In `/home/user/build_env`, you will find:
- `migrate_and_merge.py`: The legacy Python script.
- `list1.json` and `list2.json`: Two large files containing legacy v1 artifact metadata.

Your task is to:
1. Translate the exact logic of `migrate_and_merge.py` into a Go program located at `/home/user/build_env/migrate_and_merge.go`.
   - The Go program must take three positional arguments: input file 1, input file 2, and the output file path.
   - It must parse the v1 schema, migrate it to v2 (converting `size_bytes` to `size_kb` via integer division, renaming `upload_time` to `timestamp`, and adding `schema_version: 2`), merge the lists, sort them (by `timestamp` ascending, then by `id` alphabetically), and output formatted JSON (with a 2-space indent) exactly matching the Python output format.
2. Build the Go program to an executable named `/home/user/build_env/migrate_and_merge`.
3. Run the Python script to produce `/home/user/build_env/py_output.json`:
   `python3 migrate_and_merge.py list1.json list2.json py_output.json`
4. Run your new Go program to produce `/home/user/build_env/go_output.json`:
   `./migrate_and_merge list1.json list2.json go_output.json`
5. Run a diff between the two output files and save the diff output to `/home/user/build_env/verification_diff.txt`. If your translation is perfectly accurate, this file should be completely empty.

Ensure all file paths and JSON formatting exactly match the requirements.