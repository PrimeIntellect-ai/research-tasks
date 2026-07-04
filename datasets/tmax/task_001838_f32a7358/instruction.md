You are managing deployments on a Linux system where various binaries and configuration files are distributed. A configuration manager records recent deployment jobs in a structured manifest.

Your task is to write a Bash script at `/home/user/tracker.sh` that analyzes these deployed files and extracts dependency information for executable binaries.

Specifically, the script must:
1. Parse the JSON manifest file located at `/home/user/deploy.json`. This file contains an array of objects under the key `deployments`, each having an `id` (string) and a `path` (absolute path to the deployed file).
2. Iterate through each deployed file listed in the JSON.
3. Determine if the deployed file is a valid ELF executable.
4. For every file that is a valid ELF file, use `readelf` to extract the path of the "program interpreter" (the dynamic linker, e.g., `/lib64/ld-linux-x86-64.so.2`).
5. Write the extracted information to a CSV file at `/home/user/elf_deps.csv`. 

The output CSV must strictly follow this format (no headers):
`id,path,interpreter`

For example:
`dep-001,/home/user/bin/server,/lib64/ld-linux-x86-64.so.2`

Constraints:
- Use `jq` for parsing the JSON.
- Use `readelf` for parsing the ELF metadata.
- Make sure your script handles cases where files in the JSON manifest might not be ELF files (e.g., plain text or configuration files should be skipped and not appear in the CSV).
- Execute the script so the output CSV is generated.