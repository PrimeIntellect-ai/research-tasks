You are an artifact manager tasked with curating and migrating a legacy binary repository. 
You have been given a proprietary binary archive file and a binary index file located in `/home/user/legacy_repo/`. Your task is to unpack the archive using its custom format, update the configuration files within, convert the index file to a modern JSON format, and generate a summary log.

Perform the following steps:

1. **Extract the custom archive:**
   The archive is located at `/home/user/legacy_repo/artifacts.artf`. You must extract its contents to `/home/user/extracted_artifacts/` (create this directory).
   The `.artf` file format is as follows:
   - **Magic Header:** 4 bytes ASCII: `ARTF`
   - **File Count:** 2 bytes, little-endian unsigned short
   - **File Records:** For each file:
     - Filename length: 1 byte unsigned integer (`N`)
     - Filename: `N` bytes ASCII string
     - Decompressed Size: 4 bytes, little-endian unsigned integer
     - Compressed Size: 4 bytes, little-endian unsigned integer
     - Compressed Data: `Compressed Size` bytes. The compression used is a custom Run-Length Encoding (RLE). The data consists of pairs of bytes: `[count] [byte_value]`. To decompress, you repeat `byte_value` exactly `count` times.

2. **Update configurations (Text Transformation):**
   Inside the extracted files, there will be several `.cfg` files. These contain legacy network configurations. 
   Using tools like `sed`, `awk`, or Python, modify ALL `.cfg` files in `/home/user/extracted_artifacts/` in-place to apply the following updates:
   - Replace any instance of `auth_protocol=v1` with `auth_protocol=v3`
   - Replace any instance of `mirror=http://old.repo.local` with `mirror=https://new.repo.global`
   - Remove any line that starts with `deprecated_flag=`

3. **Convert the Index Format:**
   There is a binary index file located at `/home/user/legacy_repo/index.bin`. You must convert this to a JSON file at `/home/user/extracted_artifacts/index.json`.
   The `index.bin` file contains consecutive 24-byte records (no header):
   - Filename: 16 bytes ASCII, null-padded.
   - CRC32 Checksum: 4 bytes, little-endian unsigned integer.
   - Timestamp: 4 bytes, little-endian unsigned integer.
   
   The output `index.json` must be a dictionary mapping the filename (stripped of null bytes) to an object with `checksum` and `timestamp` keys.
   Example: `{"config1.cfg": {"checksum": 123456, "timestamp": 1600000000}}`

4. **Summary Log:**
   Create a log file at `/home/user/curation_summary.log` with exactly the following format (replace X with the correct integer values):
   ```
   Total files extracted: X
   Total .cfg files modified: X
   ```