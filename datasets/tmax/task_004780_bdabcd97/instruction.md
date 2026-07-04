You are an artifact manager responsible for curating an active binary repository. 

There is an incoming stream of binary artifacts and metadata files located in `/home/user/artifacts/`. A background daemon continuously writes to these files. You need to safely package the current state of a binary artifact and its metadata without risking data corruption during the read process.

Write a Python script that performs the following operations:

1. **File Locking & Binary Read:**
   Open the binary file `/home/user/artifacts/raw_data.bin`. Before reading its contents, you MUST acquire an exclusive lock using `fcntl.flock(file_descriptor, fcntl.LOCK_EX)` to ensure the background writer does not append data while you are reading. Read the entire contents into memory, and then release the lock.

2. **Custom Compression:**
   Compress the binary data using a custom Run-Length Encoding (RLE) algorithm and write the output to `/home/user/artifacts/compressed.bin`. 
   The RLE specification is:
   - For any contiguous sequence of identical bytes, output a 1-byte count followed by the 1-byte value.
   - The maximum count that can be represented in a single block is 255 (`0xFF`).
   - If a sequence exceeds 255 identical bytes, it must be split. For example, 258 consecutive `0x00` bytes becomes `0xFF 0x00 0x03 0x00`.
   - Even single bytes must be encoded as a count of 1 (e.g., a lone `0x41` becomes `0x01 0x41`).

3. **Encoding Conversion:**
   Read the text file `/home/user/artifacts/metadata.txt`. This file is encoded in `UTF-16LE`. You must decode it and extract the text.

4. **Manifest Generation:**
   Compute the SHA-256 checksum of the newly created `/home/user/artifacts/compressed.bin` file.
   Create a JSON manifest at `/home/user/artifacts/final_manifest.json` with the following exact structure:
   ```json
   {
     "metadata": "<the decoded UTF-8 string from metadata.txt>",
     "checksum": "<the hex digest of the SHA-256 hash of compressed.bin>"
   }
   ```

Write and execute this script to produce the final `compressed.bin` and `final_manifest.json` files.