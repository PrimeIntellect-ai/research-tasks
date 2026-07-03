You are an IT support technician acting on an escalated ticket (Ticket #9942). 

A critical production script `/home/user/process_config.py` crashed overnight. The sysadmins provided a memory dump from the crashed process at `/home/user/core_dump.bin`. Furthermore, the script is currently failing to run in the local environment due to a misconfiguration.

Your objective is to resolve the ticket by performing the following forensics and debugging steps:

1. **Memory Dump Analysis:** 
   The crashed process had a sensitive authentication token loaded in memory. Extract this token from `/home/user/core_dump.bin`. The token always begins with the prefix `AUTH_SEC_` followed by an alphanumeric string.

2. **Fuzz Testing:**
   The script is known to suffer from a Segmentation Fault when it receives a very specific 5-character string of lowercase English letters as its first command-line argument. Write a Python fuzzer (or a script of your choice) to test combinations and discover the exact 5-character lowercase string that causes the script to segfault (exit code 139). 

3. **Environment Misconfiguration Repair:**
   When you run the script locally with a normal input (e.g., `python3 process_config.py hello`), it fails with a configuration error instead of succeeding. Analyze the script, identify the missing environment variables and/or files, and create the necessary directory structure and files so that the script completes successfully when given a safe input.

**Deliverable:**
Once you have found the required information and fixed the local environment, create a file at `/home/user/ticket_resolution.txt` with exactly three lines in the following format:

```text
TOKEN: <extracted_token_here>
CRASH_STRING: <5_letter_crash_string>
CONFIG_DIR: <absolute_path_to_the_directory_you_configured>
```

*Note: `<absolute_path_to_the_directory_you_configured>` should be the directory path you assigned to the environment variable the script expects.*