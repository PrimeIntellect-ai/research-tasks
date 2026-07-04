As a configuration manager, you are tasked with auditing historical configuration changes across our infrastructure. We use a custom, proprietary backup format to store configuration states to save space. These backup files are scattered throughout a directory tree. 

Your task is to write a Python script that traverses the directory tree, extracts and decodes the configuration backups, and aggregates the metadata into a single CSV inventory file.

The backups are located in the directory `/home/user/sys_configs` (and its nested subdirectories). The backup files all have the extension `.ccb` (Custom Config Backup).

Each `.ccb` file is a binary file structured as follows:
1. **Magic Bytes** (4 bytes): The exact byte sequence `CCB\x01`.
2. **Timestamp** (4 bytes): An unsigned 32-bit integer, little-endian, representing the UNIX epoch timestamp of the backup.
3. **Payload Length** (4 bytes): An unsigned 32-bit integer, little-endian, representing the length of the compressed payload.
4. **Payload** (variable length): The remaining bytes are zlib-compressed data.

When you decompress the payload using standard zlib decompression, it will yield a JSON string. The JSON object has the following structure:
```json
{
  "service": "<service_name>",
  "version": "<service_version>",
  "parameters": {
    "key1": "value1",
    "key2": "value2"
  }
}
```

You must process all `.ccb` files recursively within `/home/user/sys_configs` and create a single CSV file at `/home/user/config_summary.csv`. 

The CSV file must meet the following requirements:
- The first line must be the exact header: `timestamp,service,version,param_count`
- `param_count` is the integer number of keys present inside the `"parameters"` dictionary of the JSON payload.
- The rows must be sorted primarily by `timestamp` in ascending order. If timestamps are identical, sort secondarily by `service` in alphabetical (ascending) order.
- Do not include spaces after the commas.

Write and execute the necessary script(s) to produce `/home/user/config_summary.csv`.