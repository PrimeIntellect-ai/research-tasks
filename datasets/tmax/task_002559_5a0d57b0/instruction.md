You are an integration developer working on testing a set of microservices. Your team recently inherited a mocked API service called `RustCompileAPI` which simulates a Rust compilation backend. Over time, multiple versions of API responses have been dumped into log files. 

Your task is to analyze these JSON log files using Bash tools, compare semantic versions, and generate a structural diff between the two latest versions of this specific service.

Here is what you need to do:
1. Examine all `.json` files in the directory `/home/user/api_logs/`.
2. Filter the files to process only those where the JSON field `.service` is exactly `"RustCompileAPI"`.
3. Extract the semantic version of each matching file from the `.meta.version` field.
4. Determine the **highest** (latest) semantic version and the **second-highest** semantic version among these files. (Note: standard semantic version rules apply, e.g., 1.10.0 > 1.2.0, and release candidates like 2.0.0-rc1 are evaluated accordingly).
5. For both the second-highest and the highest version files, extract the array of endpoints located at `.data.endpoints[]`.
6. Sort the endpoints alphabetically for each of the two files.
7. Create a unified diff (using `diff -u`) comparing the sorted endpoints of the **second-highest** version (the "old" file) to the sorted endpoints of the **highest** version (the "new" file).
8. Save the unified diff exactly to `/home/user/endpoint_changes.diff`.

Constraints & Formatting:
- Use standard bash tools (like `jq`, `sort`, `diff`, `grep`).
- Ensure the diff compares the raw text lists of sorted endpoints (one endpoint per line).
- Do not include timestamps or file paths in the output diff header (use `diff -u --label "old_version" --label "new_version"` or simply strip out the file paths from the standard `diff -u` output, replacing the `---` and `+++` lines with `--- old_endpoints` and `+++ new_endpoints`). Actually, to make it strict: Use `--label "second_highest" --label "highest"` for your diff.

Example of expected `diff` format:
```diff
--- second_highest
+++ highest
@@ -1,4 +1,4 @@
 /ast
+/build
 /compile
-/macro-expand
```