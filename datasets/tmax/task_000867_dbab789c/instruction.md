You are acting as a storage administrator. The application logs in `/home/user/logs` are consuming too much disk space and need to be cleaned, chunked, and archived. 

Please perform the following steps to process the logs:
1. Read all `.txt` files in `/home/user/logs` in alphabetical order.
2. Filter out and remove any lines that contain the exact string `DEBUG`.
3. Mask all IPv4 addresses in the remaining lines by replacing them with the exact string `[REDACTED]`. (Assume an IPv4 address is any sequence of four numbers separated by dots, e.g., `192.168.1.100`).
4. Split the cleaned, combined log data into chunks of exactly 50 lines each.
5. Save these chunks in a new directory called `/home/user/archive`. The files must be named `chunk_00.txt`, `chunk_01.txt`, `chunk_02.txt`, etc.
6. Write a Python script to generate a JSON manifest file at `/home/user/archive/manifest.json`. The manifest must map each chunk filename to its SHA256 checksum.

The manifest file must have the following format:
```json
{
  "chunk_00.txt": "a1b2c3d4...",
  "chunk_01.txt": "e5f6g7h8..."
}
```

Ensure the final manifest correctly reflects the state of the archived chunks.