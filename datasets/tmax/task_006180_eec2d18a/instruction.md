You are an AI assistant helping a researcher organize an incoming stream of binary dataset chunks. 

The researcher has a directory `/home/user/incoming_data` where an external process is continuously dumping binary `.dat` files. Because the writer process is concurrent, you must carefully navigate and process these files to avoid race conditions.

Your objective is to write and execute a Python script at `/home/user/organize_datasets.py` that processes these files and moves the compressed data to `/home/user/organized_data/`.

Here are the specific requirements:

1. **Safety and Synchronization**: 
   - Only process a `.dat` file if there is a corresponding empty `.ready` file with the exact same base name in the same directory (e.g., process `chunk1.dat` only if `chunk1.ready` exists). 
   - Skip files without a `.ready` marker.

2. **Binary Header Extraction**:
   Each `.dat` file has an 8-byte binary header followed by a payload.
   - Bytes 0-3: Magic number `0xDEADBEEF` (unsigned 32-bit integer, little-endian). If a file does not have this exact magic number, skip it.
   - Bytes 4-5: Class ID (unsigned 16-bit integer, little-endian).
   - Bytes 6-7: Payload length (unsigned 16-bit integer, little-endian).
   - The remaining bytes (matching the payload length) are the uncompressed data.

3. **Custom Compression (RLE)**:
   Compress the extracted payload using a custom Run-Length Encoding (RLE) scheme.
   - The output format should be a sequence of byte pairs: `[byte_value][count]`.
   - `count` is a 1-byte unsigned integer (1 to 255).
   - If a byte repeats more than 255 times consecutively, split it into multiple pairs (e.g., 256 consecutive 'A's becomes `[A][255]` followed by `[A][1]`).
   - Even a single byte is encoded as `[byte][1]`.

4. **Directory Operations & Atomic Writes**:
   - Save the compressed payload to `/home/user/organized_data/class_{class_id}/{original_filename}.rle`.
   - Create the class directories if they don't exist.
   - To prevent downstream processes from reading incomplete files, you **must** use atomic writes. Write your RLE output to a temporary file (e.g., ending in `.tmp`) in the target directory, and then rename/replace it to the final `.rle` extension.

Execute your script to process the files currently in `/home/user/incoming_data`. Do not delete the original files.