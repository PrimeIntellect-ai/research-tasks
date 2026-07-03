You are tasked with building a C++ data processing tool for a configuration management system. We receive noisy configuration file snapshots from various servers and need to normalize, sample, and report on the latest configurations per server role.

Your goal is to write a C++ program at `/home/user/config_processor.cpp`, compile it to `/home/user/config_processor`, and run it to process the data.

### Input Data
* **Raw Configs Directory**: `/home/user/raw_configs/`
* **File Naming**: `server_<id>_<role>_<timestamp>.conf` (e.g., `server_2_db_200.conf`)
* **File Format**: Messy key-value pairs (`key = value`).
  * May contain comments starting with `#` (ignore these entirely).
  * May contain leading/trailing whitespace around keys and values.
  * Keys are mixed case.

### Processing Requirements
Your C++ program must perform the following pipeline:

1. **Stratification & Sampling**: 
   Group the files by their `<role>` extracted from the filename. For each role, **only** process the single file with the highest `<timestamp>`. Ignore older files for that role.
2. **Tokenization & Normalization**:
   For the selected files, read the key-value pairs.
   * Strip all leading/trailing whitespace from keys and values.
   * Convert all **keys** to lowercase.
   * Ignore empty lines and lines starting with `#`.
   * Sort the normalized key-value pairs alphabetically by key.
3. **Template-based Generation**:
   Read the template file at `/home/user/report_template.txt`.
   For each processed role (sorted alphabetically by role name), substitute the placeholders and append the result to `/home/user/config_report.md`.
   * `{{ROLE}}` -> The server role.
   * `{{TIMESTAMP}}` -> The highest timestamp.
   * `{{SERVER_ID}}` -> The server ID associated with that file.
   * `{{CONFIG_PAIRS}}` -> The normalized config pairs, one per line, in `key=value` format (no spaces around `=`).
4. **Pipeline Logging**:
   As you generate the report for each role (in alphabetical order of the roles), append a log line to `/home/user/pipeline.log` exactly in this format:
   `[INFO] Processed <filename>: <N> valid keys found.`

Compile your C++ program using `g++ -std=c++17 /home/user/config_processor.cpp -o /home/user/config_processor` and execute it.