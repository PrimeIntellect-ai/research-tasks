You are tasked with automating a configuration and firmware update process for an embedded system simulator. 

You need to write and execute a Python script at `/home/user/apply_update.py` that performs the following steps:

1. **Archive Verification**: 
   You are provided with a firmware update archive at `/home/user/update.zip` and its expected SHA-256 checksum at `/home/user/update.zip.sha256`. Your script must first verify the SHA-256 hash of the zip file. If the hash does not match, the script must print an error and exit with code 1.

2. **Extraction and Parsing**:
   Extract the zip file to a temporary directory. Inside, you will find two files: `changes.wal` (a Write-Ahead Log) and `firmware.elf`.

3. **Applying Configuration Changes (Atomic Write)**:
   The `changes.wal` file contains configuration updates. Each line is formatted as `TXN_ID:ACTION:KEY[:VALUE]`, where:
   - `TXN_ID` is an integer transaction ID.
   - `ACTION` is either `SET` or `DELETE`.
   - `KEY` is the configuration key.
   - `VALUE` is the value to set (always treated as a string; only present for `SET`).
   
   The lines in the WAL file might be out of order. You must apply the changes to the existing configuration file at `/home/user/config.json` in strictly ascending order of `TXN_ID`. 
   To prevent corruption in case of failure, you must use an atomic write approach to update `/home/user/config.json` (i.e., write to a temporary file in the same directory and safely replace the original file).

4. **ELF Metadata Extraction**:
   Parse the extracted `firmware.elf` file to extract specific metadata. You must extract:
   - The Entry Point address, formatted as a hexadecimal string (e.g., `"0x401000"`).
   - The size in bytes of the `.text` section, as an integer.
   *(Hint: You may install and use libraries like `pyelftools` for this).*

5. **Summary Generation**:
   Finally, your script must generate a YAML summary file at `/home/user/summary.yaml` with the following exact structure:
   ```yaml
   firmware:
     entry_point: "<extracted_hex_string>"
     text_size: <extracted_integer>
   config_keys:
     - <key1>
     - <key2>
     ...
   ```
   The `config_keys` list must contain all the keys present in the updated `config.json`, sorted alphabetically.

Ensure you install any necessary Python packages and run your script to leave the system in the final requested state (with updated `config.json` and `summary.yaml` created).