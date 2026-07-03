You are helping a data researcher extract and verify a custom dataset archive. The researcher has received a custom text-based archive format containing compressed files, but standard tools cannot parse it.

The archive is located at `/home/user/dataset.txt`.

The custom archive format is a plain text file structured as follows:
1. It begins with a magic string `RSCH_ARCHIVE_V1` on the first line.
2. The rest of the file consists of sequential file records. Each record has exactly 4 lines:
   - Line 1: `FILE:<filename>` (e.g., `FILE:data1.csv`)
   - Line 2: `SHA256:<hash>` (The SHA256 hex digest of the **uncompressed** file data)
   - Line 3: `SIZE:<bytes>` (The size in bytes of the hex-encoded string on the next line)
   - Line 4: `<hex_encoded_zlib_data>` (The zlib-compressed file data, encoded as a hexadecimal string)

Your task:
1. Write a Go program at `/home/user/extract.go` that parses `/home/user/dataset.txt`.
2. For each file record in the archive:
   - Decode the hex data.
   - Decompress the zlib data.
   - Compute the SHA256 hash of the uncompressed data.
   - Compare the computed hash with the provided hash to verify archive integrity.
   - If the hash matches, save the uncompressed data to `/home/user/extracted/<filename>`.
   - If the hash DOES NOT match (corrupted), do NOT save the file. Instead, append the `<filename>` to `/home/user/corrupted.log` (one filename per line).
3. Run your Go program to perform the extraction.

Make sure to create the `/home/user/extracted` directory before saving files to it.