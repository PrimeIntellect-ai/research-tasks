You are a compliance analyst tasked with generating an audit trail for a set of internal executable files before they are approved for deployment. Some legacy binaries might contain insecure function calls and need to be flagged for strict process isolation.

Your task is to write a Python script at `/home/user/audit.py` that performs an automated vulnerability scan and binary analysis on all files located in the `/home/user/binaries/` directory.

The Python script must:
1. Iterate through all files in `/home/user/binaries/`.
2. Determine if the file is a valid ELF executable. (If it is not an ELF file, it should still be included in the final report, but flagged as safe).
3. For valid ELF files, analyze their symbol tables to determine if they import or use the insecure C standard library function `gets`.
4. Generate an audit trail report located at `/home/user/audit_report.json`. The output must be a JSON array of objects, sorted alphabetically by the `filename`. Each object must have the following exact keys:
   - `"filename"`: The string name of the file (e.g., "legacy_app").
   - `"uses_insecure_gets"`: A boolean (`true` or `false`) indicating if the `gets` symbol was found in the binary. If the file is not a valid ELF, this should be `false`.

Additionally, to satisfy our process isolation policy, your script must automatically generate a lightweight sandbox wrapper script for *only* the binaries that are flagged as using `gets` (`uses_insecure_gets: true`). 
For each vulnerable binary, create an executable bash script at `/home/user/sandbox_<filename>.sh`. 
This wrapper script must:
1. Use `ulimit -c 0` to disable core dumps (preventing memory leaks on crashes).
2. Execute the target binary using `env -i` to completely clear the environment variables, providing basic sandboxing.
3. Pass any arguments provided to the wrapper script directly to the binary.
4. Have executable permissions set (`chmod +x`).

Run your `audit.py` script to generate the JSON report and the necessary wrapper scripts.