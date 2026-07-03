You are an AI assistant acting as a configuration manager. We need to track configuration state changes across several applications based on raw backup data.

You have been provided with a nested archive at `/home/user/backups/infra_state.tar.gz`. This archive contains `.tar.bz2` files for different applications (e.g., `app_alpha.tar.bz2`, `app_beta.tar.bz2`).

Inside each application's `.tar.bz2` archive, you will find:
1. `servers.conf` - A poorly formatted text file. It contains server IP addresses, but has leading/trailing spaces, empty lines, and inline comments (anything following a `;`).
2. `state.bin` - A custom binary dump of the application's configuration state.
3. `changes.log` - A multi-line text log of configuration changes.

Your task is to:
1. Write a bash script `/home/user/extract_and_clean.sh` to:
   - Extract the outer `infra_state.tar.gz` and all inner `.tar.bz2` archives into `/home/user/extracted/`.
   - Use `sed`, `awk`, or similar tools to clean all `servers.conf` files in place. The cleaned files must contain only the raw IP addresses, one per line, with no whitespace, empty lines, or comments.

2. Create a Rust project in `/home/user/state_parser` that reads the extracted files and produces a summary.
   - **Binary Format (`state.bin`)**: 
     - First 4 bytes: Magic header `0x43 0x46 0x47 0x01` (`CFG\x01`).
     - Next 4 bytes: Little-endian 32-bit unsigned integer `N` representing the number of records.
     - Following `N` records: 
       - 1 byte unsigned integer `K_LEN` (Key length).
       - `K_LEN` bytes UTF-8 string (Key).
       - 4 bytes Little-endian 32-bit unsigned integer `VERSION` (Configuration version number).
   - **Multi-line Log Format (`changes.log`)**:
     - Records are separated by a line containing exactly `---`.
     - Each record starts with a line `Commit: <hash>`.
     - Following lines contain metadata like `Author: <name>`.
     - You must count the total number of commits made by the author "admin" across all logs.

3. The Rust program must output a single JSON file to `/home/user/report.json` with the following schema:
```json
{
  "admin_commits": <integer_total_admin_commits>,
  "apps": {
    "app_alpha": {
      "servers": ["ip1", "ip2"],
      "config_keys": {
        "<key_name>": <version_integer>
      }
    },
    ...
  }
}
```
*Note: The `servers` array must come from the cleaned `servers.conf`. The `config_keys` object must come from parsing `state.bin`. The keys in `apps` must match the application archive names (without the `.tar.bz2` extension).*

Ensure you compile and run your Rust program to generate the final `/home/user/report.json`.