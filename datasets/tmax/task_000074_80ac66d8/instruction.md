You are tasked with helping our configuration management system track changes across legacy binary configuration files. 

Our legacy application uses a custom binary format to store its configurations. You are provided with two configuration files: `/home/user/config_v1.bin` and `/home/user/config_v2.bin`.

Your goal is to write a Python script that reads both binary files, extracts their contents, compares them, and outputs the differences to a JSON file at `/home/user/diff.json`.

**Binary Format Specification:**
1. **Magic Header:** 4 bytes ASCII string `CONF`.
2. **Version:** 1 byte unsigned integer (always `0x01`).
3. **Record Count:** 2 bytes unsigned short, little-endian, representing the number of key-value pairs.
4. **Records:** For each record (sequentially):
    - **Key Length:** 1 byte unsigned integer.
    - **Key:** ASCII string of length specified above.
    - **Value Type:** 1 byte unsigned integer (`0x01` means 32-bit integer, `0x02` means string).
    - **Value:** 
        - If type is `0x01` (Integer): 4 bytes signed integer, little-endian.
        - If type is `0x02` (String): 2 bytes unsigned short (little-endian) representing the string length, followed by the ASCII string itself.

**Comparison and Output Specification:**
Your script must compare `config_v1.bin` (old) and `config_v2.bin` (new). 
Generate a JSON file at `/home/user/diff.json` containing only the keys that have changed, been added, or been removed.

The output JSON must strictly follow this structure:
```json
{
  "key_name": {
    "status": "modified", 
    "old_value": 123,
    "new_value": 456
  },
  "new_key": {
    "status": "added",
    "old_value": null,
    "new_value": "some_string"
  },
  "deleted_key": {
    "status": "removed",
    "old_value": 789,
    "new_value": null
  }
}
```
- Use the exact string literals `"added"`, `"removed"`, or `"modified"` for the `status` field.
- Keys that are identical in both files should NOT be included in `diff.json`.
- Do not use any external Python libraries (like `pandas` or `construct`); standard library modules like `struct` and `json` are sufficient.