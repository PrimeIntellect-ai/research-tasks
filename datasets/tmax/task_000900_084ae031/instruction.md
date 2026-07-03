You are acting as a backup administrator. You have inherited a directory of custom split-backup files that need to be merged to restore the original archived data.

The backup files are located in `/home/user/backups/`. The files have a `.dat` extension, but their filenames do not indicate their proper order. 

Each file contains a custom binary header followed by a chunk of the backup payload. The binary format of each file is exactly as follows:
- **Bytes 0-10 (11 bytes):** Magic string `ARCHIVE_BKP` (in ASCII).
- **Byte 11 (1 byte):** Unsigned 8-bit integer representing the Chunk Sequence ID (e.g., 0, 1, 2...).
- **Bytes 12-15 (4 bytes):** Unsigned 32-bit integer (Little Endian) representing the Payload Size in bytes.
- **Bytes 16+:** The actual raw payload data for this chunk.

Your task:
1. Write a Go program at `/home/user/restore.go` that parses all `.dat` files in `/home/user/backups/`.
2. Extract the Chunk Sequence ID and the payload from each file.
3. Merge the payloads together in the correct sequential order (starting from ID 0) into a single output file located at `/home/user/restored_data.bin`.
4. Run your Go program.
5. Once the data is successfully restored, create a text file at `/home/user/metrics.log` containing only the total number of combined payload bytes restored.

Ensure your code validates the magic string and strictly reads only the number of payload bytes specified in the header to avoid reading trailing garbage.