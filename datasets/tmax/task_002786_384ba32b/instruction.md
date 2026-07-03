You are acting as a backup administrator. We are migrating our infrastructure and need to decommission an old, proprietary backup manifest generator written in C. We have lost the original source code, but we still have the compiled, stripped binary.

Your task is to write a Python 3 script that perfectly replicates the behavior of this legacy binary.

**Legacy Tool Details:**
- Path: `/app/legacy_backup_tool`
- Usage: `/app/legacy_backup_tool <path_to_config.json> <target_directory>`
- Output: Writes a proprietary binary manifest of the target directory to `stdout`.

**Configuration:**
The tool reads a JSON configuration file that dictates its behavior. The JSON has the following structure:
```json
{
  "ignore_extensions": [".tmp", ".log"],
  "follow_symlinks": false,
  "extract_header_bytes": 16
}
```

**What you need to do:**
1. Analyze the `/app/legacy_backup_tool` binary to understand the binary format it outputs. You can run it against dummy directories to inspect its output using `xxd` or `hexdump`.
2. Determine how it handles:
   - Directory traversal (e.g., sorting order of files).
   - Symbolic links (based on `follow_symlinks`).
   - Checksum generation.
   - Binary header extraction (grabbing the first `extract_header_bytes` of a file, handling files smaller than this value).
3. Write your replacement script at `/home/user/new_backup_tool.py`.
4. Your script must accept the exact same arguments (`<config.json>` `<target_directory>`) and output the **exact same bit-for-bit binary data** to `stdout` as the legacy tool for any valid input directory and configuration. 

Do not rely on the legacy tool from within your Python script (e.g., no `subprocess.run`). You must reimplement the logic natively in Python. Ensure your script gracefully handles binary file contents, text formats, and symlinks.