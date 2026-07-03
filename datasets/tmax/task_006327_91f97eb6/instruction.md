You are assisting a researcher who is organizing datasets. The researcher received a dataset archive in a custom format (`/home/user/dataset.carch`), but the tool used to create this archive is known to have a path traversal (Zip Slip) vulnerability, and the text encoding is specific to older Japanese systems.

Your task is to write a Python script that parses `/home/user/dataset.carch` and extracts its contents safely into the directory `/home/user/extracted/`. 

The `.carch` file is a plain text file where each embedded file is represented by four lines:
1. `FILE: <filepath>`
2. `SIZE: <original_uncompressed_byte_size>`
3. `ENCODING: <character_encoding>`
4. `DATA: <base64_encoded_zlib_compressed_data>`

Requirements for your extraction script:
1. **Security (Path Traversal Mitigation)**: Read the `FILE:` path. If the path attempts to break out of the extraction directory using directory traversal (e.g., contains `../`), you must mitigate this by extracting the file using *only its basename*, placing it directly into `/home/user/extracted/`.
2. **Custom Decompression & Encoding**: For the `DATA:` line, you must base64-decode the string, decompress it using `zlib`, decode the bytes using the encoding specified in the `ENCODING:` line, and finally save the text to disk as `UTF-8`.
3. **Atomic Writes**: To prevent corrupted data from concurrent access, write the extracted UTF-8 text to a temporary file (e.g., `<filename>.tmp`) first, and then atomically rename it to the final filename.
4. **Manifest Generation**: After all files are safely extracted, generate a SHA-256 manifest file at `/home/user/manifest.txt`. Each line must be formatted exactly as `<sha256_hex>  <basename>`, sorted alphabetically by the filename. The hashes must be calculated from the final extracted UTF-8 files.

Ensure the final extracted files are stored in `/home/user/extracted/`. Do not leave any `.tmp` files behind.