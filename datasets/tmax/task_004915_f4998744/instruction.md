I need you to write a Python utility to parse a proprietary archive dump format used in our project's legacy backup system. The backup dumps frequently contain cyclic symlink definitions that crashed our old parser, so we need a robust script that scans the raw backup binaries.

Create a script at `/home/user/parse_dump.py`. 

The script must accept a single command-line argument: the path to a binary dump file. 
You must use memory-mapped I/O (`mmap`) or efficient streaming to process the file, as these dumps can theoretically be larger than available RAM.

**Dump Format Specification:**
The file contains zero or more records interspersed with random garbage bytes. You must scan the file to find valid records.
A valid record is structured as follows:
1. **Magic Header:** A 2-byte marker.
2. **Payload Length:** A 4-byte unsigned integer (Little Endian) representing the length of the JSON payload.
3. **Payload:** The JSON string (utf-8 encoded) of exactly the length specified above.
4. **Checksum:** A 4-byte unsigned integer (Little Endian) representing the CRC32 checksum of the payload concatenated with a secret salt.

**Verification Rules:**
- You must verify the integrity of each record. The checksum is calculated as: `zlib.crc32(payload_bytes + salt_bytes) & 0xFFFFFFFF`.
- The Magic Header bytes and the secret Salt value are documented in a screenshot of an old whiteboard session, located at `/app/backup_specs.png`. You will need to extract these values from the image.
- The JSON payload contains a dictionary with keys `file_id`, `path`, and `symlink_target`. 
- If a record's checksum is invalid, or if parsing the JSON fails, skip it and continue searching for the next Magic Header.

**Output:**
Your script must output a strictly formatted CSV to `stdout` containing the valid records. 
The CSV must have the following headers: `file_id,path,symlink_target`.
Only include records that pass the checksum verification. Print the CSV rows in the order they appear in the binary file.

Ensure the script handles edge cases gracefully, such as truncated records at the end of the file.