You are a script developer tasked with creating a local CI/CD pre-commit utility to ensure shared libraries meet strict ABI and compatibility constraints before they are packaged.

In the directory `/home/user/project`, you will find:
1. A compiled shared library: `/home/user/project/plugin.so`
2. A configuration file: `/home/user/project/rules.json`

The `rules.json` file contains structured data specifying ABI constraints. It looks like this:
```json
{
  "max_glibc_version": "2.30",
  "required_exports": ["compute", "initialize"]
}
```

Write a Bash script at `/home/user/project/check_abi.sh` that takes exactly two arguments: the path to the shared object file and the path to the JSON rules file.
Your script must perform the following:
1. Parse the JSON file to extract the `max_glibc_version` and the list of `required_exports`.
2. Analyze the provided `.so` file to find the highest `GLIBC_X.Y` version required by its dynamic symbols (you can use tools like `objdump` or `nm`).
3. Analyze the `.so` file to ensure all function names listed in `required_exports` are exported as global text symbols (type 'T' in `nm`).
4. Evaluate the constraints: 
   - The highest GLIBC version detected in the `.so` file must be less than or equal to `max_glibc_version` (use version sort `-V` for comparison).
   - All required symbols must be present.
5. Generate a validation report at `/home/user/project/report.json` with the following exact structure:
```json
{
  "status": "PASS",
  "highest_glibc_detected": "2.2.5",
  "missing_exports": []
}
```
If the library fails any constraints, `status` must be `"FAIL"`, and `missing_exports` should be a JSON array of strings containing the names of any required exports that were not found (if all were found, it should be empty). The script should exit with code 0 if constraints are met, and 1 if they are violated.

Create the script, make it executable, and run it against the files in `/home/user/project` to generate the `report.json` file.