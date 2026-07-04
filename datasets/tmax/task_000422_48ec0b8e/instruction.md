You are an incident responder investigating a potential security breach on a Linux server. We suspect a background worker script was poorly configured and leaked a sensitive authentication token via its command-line arguments, which were captured in a process monitoring log. The script also references a suspicious ELF binary payload.

Your task is to analyze the artifacts and generate an automated incident report using Python. 

Here are the details of your investigation:
1. Examine the process monitoring log located at `/home/user/process_dump.log`. Identify the running process that leaked its authentication token via the `--auth-token=` argument.
2. The same process command line will indicate the path to a suspicious binary via the `--target=` argument. Locate this ELF file.
3. Perform a file integrity and binary format analysis on the suspicious ELF file:
   - Calculate its SHA256 checksum.
   - Determine its target architecture (e.g., Advanced Micro Devices X86-64, Intel 80386, AArch64, etc., as output by `readelf -h` or `file`).
4. Write a Python script at `/home/user/generate_report.py` that, when executed without arguments, produces a JSON file at `/home/user/incident_report.json` containing your findings.

The `/home/user/incident_report.json` must have exactly the following structure:
```json
{
  "leaked_token": "<the exact token extracted from the log>",
  "payload_path": "<the absolute path of the target payload>",
  "payload_sha256": "<the 64-character SHA256 hash of the payload>",
  "elf_architecture": "<the machine architecture string, e.g., 'Advanced Micro Devices X86-64'>"
}
```

Write the Python script, execute it to generate the JSON report, and ensure all fields are correctly populated based on the artifacts present in the system.