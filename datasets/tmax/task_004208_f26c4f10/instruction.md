You are a storage administrator responsible for managing disk space on a legacy logging server. The server uses a custom Write-Ahead Log (WAL) format. Due to a recent storage appliance crash, many of these WAL archives are corrupted.

You have received an automated video alert from the storage dashboard, located at `/app/alert.mp4`. This video encodes a crucial configuration parameter: the exact number of pure white frames (rgb: 255, 255, 255) in the video represents the expected "Block Alignment Value" (BAV) for your storage cluster.

Your task is to write a standalone, executable CLI tool at `/home/user/wal_checker` that verifies the integrity of these WAL files so we can safely delete corrupted ones. You may write this tool in Bash, Python, C, or any combination of standard languages, but it must be executable directly.

### Tool Specification: `/home/user/wal_checker`
Your tool must accept exactly one argument: the absolute path to a WAL file.
It must parse the binary file, output a single specific string to `stdout`, and exit with code 0. 

**Format & Validation Rules:**
1. **Header (6 bytes):**
   - Bytes 0-2: Magic string `WAL` (ASCII)
   - Byte 3: Version (Must be `0x01`)
   - Bytes 4-5: BAV (Little-endian 16-bit unsigned integer).
   - *Rule:* If the magic string or version is wrong, output `INVALID_HEADER` and exit.
   - *Rule:* If the BAV in the header does NOT perfectly match the number of pure white frames you extracted from `/app/alert.mp4`, output `INVALID_BAV` and exit.
2. **Records (Repeated until EOF):**
   - Immediately following the header are the records.
   - Bytes 0-3: Data Length `L` (Little-endian 32-bit unsigned integer).
   - Bytes 4 to `4+L-1`: The raw data payload.
   - Next 4 bytes: Expected CRC32 checksum of the raw data payload (Little-endian 32-bit unsigned integer). *Note: Use standard IEEE 802.3 CRC32.*
   - *Rule:* If a record's computed CRC32 does not match the stored CRC32, or if the file ends prematurely before a full record (length, data, and checksum) can be read, output `CORRUPT` and exit immediately.
3. **Success:**
   - If the header is valid, BAV matches, and all records are fully intact and pass their CRC32 checks (or if there are zero records but the header is valid), output `SAFE` and exit.

**Example Invocations:**
```bash
$ /home/user/wal_checker /data/logs/001.wal
SAFE
$ /home/user/wal_checker /data/logs/002.wal
INVALID_BAV
```

Determine the BAV from the video, implement the robust parsing logic in `/home/user/wal_checker`, and ensure it handles arbitrary binary data, edge cases, and sudden EOFs gracefully without crashing.