You are assisting a backup administrator. We have a proprietary backup archive system that generates `.bak` files. Recently, we suspect that some of these archives were maliciously crafted to include directory traversal payloads (similar to a "zip slip" vulnerability) to overwrite files outside the intended extraction directory.

Your task is to write a C++ program that parses these custom binary archive files, extracts the file path metadata, and generates a structured JSON report identifying any dangerous paths.

Here is the specification for the `.bak` custom binary format:
1. **Magic Bytes**: The first 4 bytes are exactly the ASCII characters `BAK1`.
2. **Entry Count**: The next 4 bytes represent the number of file entries in the archive as an unsigned 32-bit integer (little-endian).
3. **Entries**: For each entry, the following structure applies sequentially:
   - **Path Length**: 2 bytes representing the length of the file path as an unsigned 16-bit integer (little-endian).
   - **File Path**: The string representing the file path (length is determined by the previous field). Not null-terminated.
   - **File Size**: 4 bytes representing the size of the file data as an unsigned 32-bit integer (little-endian).
   - **File Data**: The actual file content, which is exactly "File Size" bytes long. You must skip over this data to read the next entry.

You need to search the directory `/home/user/backups/` for all files ending in `.bak`.
For each archive, parse the header and entries to extract the file paths. Check each path to determine if it is "dangerous".
A path is considered **dangerous** if it meets either of these conditions:
- It starts with a forward slash `/` (an absolute path).
- It contains the substring `../` anywhere in the path.

Write and execute a C++ program that performs this analysis and outputs the results to a file at `/home/user/report.json`.

The output file `/home/user/report.json` must be valid JSON with the following structure:
```json
{
  "filename1.bak": {
    "total_entries": 3,
    "dangerous_paths": [
      "../etc/passwd",
      "/var/run/secret"
    ]
  },
  "filename2.bak": {
    "total_entries": 2,
    "dangerous_paths": []
  }
}
```
Only include the base filename (e.g., `archive.bak`, not the full path `/home/user/backups/archive.bak`) as the keys in the JSON. If a file does not have the `BAK1` magic bytes, you should ignore it and not include it in the JSON report. Ensure your C++ program is robust against malformed or truncated files (safely skip or ignore if out-of-bounds).