You are an infrastructure engineer acting as a configuration manager. You need to track configuration drift across a fleet of servers by analyzing their backed-up configuration files.

The backups are stored in `/home/user/configs/`. Due to historical reasons, the configuration files are in three different formats: JSON (`.json`), XML (`.xml`), and INI (`.ini`).

Your task is to write a Bash script at `/home/user/audit.sh` that extracts the `port` and `memory` settings from all configuration files, normalizes the memory values, and outputs a consolidated CSV report.

**Data Formats:**
1. **JSON (`.json`)**: Contains an object with a nested `app` object containing `port` (integer) and `memory` (string, e.g., "512M" or "2G").
   Example: `{"app": {"port": 8080, "memory": "1G"}}`
2. **XML (`.xml`)**: Contains a `<config>` root element with an `<app>` child, containing `<port>` and `<memory>` elements.
   Example: `<config><app><port>8081</port><memory>512M</memory></app></config>`
3. **INI (`.ini`)**: Contains an `[app]` section with `port=` and `memory=` key-value pairs.
   Example:
   ```
   [app]
   port=8082
   memory=4G
   ```

**Requirements for `/home/user/audit.sh`:**
1. Read all files in `/home/user/configs/`.
2. Extract the `port` and `memory` values.
3. Normalize the `memory` value to an integer representing Megabytes (MB).
   - If the value ends in `M`, strip the `M` (e.g., `512M` -> `512`).
   - If the value ends in `G`, strip the `G` and multiply by `1024` (e.g., `2G` -> `2048`).
4. Generate a CSV file at `/home/user/config_audit.csv` with the exact header: `filename,format,port,memory_mb`.
   - `filename`: The base name of the file (e.g., `server_001.json`).
   - `format`: The extension of the file without the dot (`json`, `xml`, or `ini`).
   - `port`: The extracted port number.
   - `memory_mb`: The normalized memory in MB.
5. Sort the data rows (excluding the header) alphabetically by `filename`.
6. Implement parallel data processing in your script (e.g., using background jobs `&`, `xargs -P`, or `parallel`) to ensure it scales if thousands of files were present.
7. Run your script to generate the final `/home/user/config_audit.csv`.

Ensure your script is executable and handles all extraction natively using standard Linux utilities (`jq` is installed and available for JSON parsing).