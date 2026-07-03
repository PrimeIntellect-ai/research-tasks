You are a senior log analyst tasked with modernizing a fragile data pipeline. 

Your organization uses a legacy data ingestion validator, located at `/app/legacy_validator`. This is a compiled, stripped C binary that takes a JSON-Lines log file as an argument. It exits with code `0` if the log file is considered "valid", and either crashes (segfaults) or exits with code `255` if the log file contains anomalies. 

The binary is undocumented, but your preliminary analysis suggests it enforces strict rules around:
1. **Character Encoding:** It specifically crashes on certain malformed Unicode escape sequences within JSON strings.
2. **Chronological Consistency:** It flags files where logs for a given entity travel backward in time.
3. **Imputation Feasibility:** It rejects files where missing data points cannot be safely interpolated due to excessive time gaps.

Your task is to create a robust, multi-language wrapper or replacement script at `/home/user/detector.sh` that perfectly mirrors the binary's validation logic without crashing. 

**Requirements:**
1. Your entry point must be an executable script located at `/home/user/detector.sh`.
2. It must accept exactly one argument: the path to a JSONL log file.
    * Example: `/home/user/detector.sh /path/to/logfile.jsonl`
3. It must print exactly `CLEAN` to standard output if the file is valid according to the legacy binary's rules, or `EVIL` if it violates them (would cause a crash or exit code 255).
4. The JSONL files contain the following fields: `host_id` (string), `timestamp` (ISO-8601 string), `message` (string), and `metric` (float or null).
5. You must reverse-engineer the exact rules by interacting with the `/app/legacy_validator` binary. You can use any tools available in the environment (`objdump`, `strings`, `python3`, `gdb`, etc.) to analyze it or fuzz it to discover the exact rules for Unicode anomalies, timestamp alignment, and sorting/grouping constraints.
6. Your script should be robust and handle files containing millions of lines efficiently (utilize efficient sorting, regex, and streaming techniques).

Do not rely on the legacy binary in your final script, as it is slated for deprecation. Your script must independently classify the files.