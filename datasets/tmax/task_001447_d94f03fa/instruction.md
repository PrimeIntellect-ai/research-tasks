You have just inherited a legacy data processing pipeline from a departed developer. The system parses server request logs, but it has started crashing intermittently. Furthermore, the developer left behind a memory dump from a crashed service, which contains an authorization token we need to recover.

Your task is to perform forensics on this system and fix the pipeline.

**System State:**
- `/home/user/legacy_processor.sh`: The Bash script responsible for processing CSV logs. It is currently failing on some inputs.
- `/home/user/raw_data.csv`: A sample input log file containing some edge cases.
- `/home/user/memory.dmp`: A mock binary memory dump file from the crashed application.

**Instructions:**
1. **Memory Dump Analysis:** Analyze `/home/user/memory.dmp` to extract a lost authorization token. The token is stored in the format `AUTH_TOKEN=<alphanumeric_string>`. Extract ONLY the `<alphanumeric_string>` value and save it to `/home/user/token.txt`.
2. **Minimal Reproducible Example:** Identify the exact edge case causing `/home/user/legacy_processor.sh` to crash (exit code > 0). Create a file named `/home/user/mre.csv` containing EXACTLY ONE line of CSV data that reproduces this crash.
3. **Format Parsing Edge-case Repair:** Modify `/home/user/legacy_processor.sh` to handle this edge case gracefully. If the field causing the crash is missing or not a valid number, the script should output `INVALID: <req_id>` and continue processing the rest of the file without crashing.
4. **Validation:** Run your repaired `/home/user/legacy_processor.sh` on `/home/user/raw_data.csv` and save the standard output to `/home/user/fixed_output.txt`.

Ensure all requested output files (`/home/user/token.txt`, `/home/user/mre.csv`, `/home/user/fixed_output.txt`) are created exactly as specified.