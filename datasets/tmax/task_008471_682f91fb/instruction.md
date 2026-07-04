You are acting as a localization engineer. Our translation management system has been dumping daily JSON-Lines (`.jsonl`) logs of translation updates into `/home/user/loc_drops/`. 

However, the logging system has a bug: it sometimes writes malformed unicode escape sequences in the JSON values (e.g., `\u12G4` or `\uXYZ1` instead of valid hex digits). Standard JSON parsers break completely on these lines.

Your task is to build a robust, parallelized data processing pipeline in Python to clean, parse, aggregate, and export these translations, and then schedule it.

Here are the requirements:

1. **Python Pipeline (`/home/user/process_locs.py`)**
   - Must use Python's `multiprocessing` or `concurrent.futures` to process all `.jsonl` files in `/home/user/loc_drops/` in parallel.
   - **Data Cleaning:** Before parsing each line as JSON, you must find any invalid unicode escape sequences (a literal `\` followed by `u` followed by exactly 4 characters where at least one character is NOT a valid hexadecimal digit `0-9a-fA-F`). Replace the `\u` and those 4 characters entirely with the string `[ERR]`.
   - **Parsing:** Parse the cleaned line as JSON. The JSON looks like: `{"timestamp": "2023-10-25T14:32:01Z", "lang": "es-ES", "key": "ui_login_btn", "value": "Iniciar sesi\u00f3n"}`
   - **Time-based Bucketing:** Group the parsed records by the date portion of the `timestamp` (YYYY-MM-DD) and the `lang`.
   - **Multi-format Output:** For each Date and Language combination, create a directory `/home/user/processed/<YYYY-MM-DD>/` and write the following 3 files:
     - `lang_<lang>.csv`: A CSV file with headers `key,value`.
     - `lang_<lang>.parquet`: A Parquet file with columns `key,value` (you may need to install `pandas` and `pyarrow`).
     - `lang_<lang>.xml`: An Android-style XML file formatted exactly like this:
       ```xml
       <?xml version="1.0" encoding="utf-8"?>
       <resources>
           <string name="<key>"><value></string>
           ...
       </resources>
       ```
       (Do not escape the `<value>` in the XML beyond standard XML entity escaping if you use a standard library, but ensure the structure matches).

2. **Pipeline Execution & Scheduling**
   - Write a bash script `/home/user/run_pipeline.sh` that executes your Python script. Ensure it has execute permissions.
   - Install a cron job for the user `user` that runs `/home/user/run_pipeline.sh` every day at 2:00 AM.
   - Run your Python script once manually so the outputs in `/home/user/processed/` are generated.

Your final state will be verified by checking the contents of `/home/user/processed/`, verifying the formats, and inspecting the crontab.