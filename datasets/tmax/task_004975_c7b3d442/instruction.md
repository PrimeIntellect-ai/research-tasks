You are assisting a technical writer in migrating away from a legacy, undocumented documentation processing tool. The technical writer has a legacy utility located at `/app/doc_encoder` (a stripped Linux binary). This utility reads raw documentation text from standard input (`stdin`) and writes a custom compressed binary format to standard output (`stdout`). 

Because this binary is old and unmaintainable, the writer needs a pure Python 3 replacement script located at `/home/user/encoder.py`. Your script must be a **bit-exact drop-in replacement** for `/app/doc_encoder`.

Through some initial reverse-engineering, we know the legacy tool uses a custom streaming compression format with the following structure:
1. **Magic Header**: The ASCII string `DOCX` (4 bytes).
2. **Original Length**: A 4-byte unsigned integer (little-endian) representing the length of the uncompressed input in bytes.
3. **Checksum/Key**: A 1-byte value calculated as the sum of all bytes in the uncompressed input modulo 256. (For an empty file, this is 0).
4. **Compressed Payload**: The input data is compressed using a simple Run-Length Encoding (RLE). 
   - Each RLE block consists of exactly 2 bytes: `[count][byte]`.
   - The `count` is a 1-byte unsigned integer representing the number of times the `byte` is repeated. It can range from 1 to 255. (If a character repeats more than 255 times, it is split into multiple RLE blocks).
   - Before this RLE data is written to the file, **every byte** of the RLE payload (both the `count` bytes and the `data` bytes) is XOR'd with the 1-byte **Checksum/Key**.

Write `/home/user/encoder.py` to read all bytes from `sys.stdin.buffer`, apply this exact encoding scheme, and write the binary result to `sys.stdout.buffer`. 

You can test your implementation by creating sample text files and comparing the output of your script with the output of `/app/doc_encoder`.