You are tasked with analyzing historical configuration changes for a server fleet. All historical states have been packaged into a single master archive located at `/home/user/server_history.tar`. 

Inside this master tarball, there are several nested archives named `state_01.tar.gz`, `state_02.tar.gz`, etc., representing different points in time.

Your objective is to write and execute a Python script that tracks how a specific configuration value changed over time, adhering to the following strict constraints:

1. **In-Memory Processing**: The master archive `server_history.tar` is theoretically too large to extract to disk. Your Python script MUST process the master archive and its nested `.tar.gz` archives entirely in memory using streaming or file-object I/O (e.g., using Python's `tarfile` module). You are not allowed to extract the archives to disk.
2. **Integrity Verification**: Some of the nested `.tar.gz` archives might be corrupt. Your script must detect and gracefully skip any invalid or corrupt nested archives.
3. **Directory Traversal**: Inside each valid nested archive, there is a configuration file named exactly `settings.conf`. Its path varies depending on the snapshot (e.g., it might be in `etc/app/`, `opt/service/`, etc.). Your script must search through the nested archive's structure to find it.
4. **Data Extraction**: Once `settings.conf` is found, parse it to extract the integer value of `MAX_CONNECTIONS`. (The file contains key-value pairs in the format `KEY=VALUE`).

**Output Verification:**
Your script must generate a JSON file at `/home/user/connection_history.json`. 
The JSON file should contain a single dictionary mapping the name of the valid nested archive (e.g., `"state_01.tar.gz"`) to its corresponding integer value for `MAX_CONNECTIONS` (e.g., `100`). Corrupt archives should be entirely omitted from this JSON file.

Example output format for `/home/user/connection_history.json`:
```json
{
  "state_01.tar.gz": 100,
  "state_03.tar.gz": 250
}
```