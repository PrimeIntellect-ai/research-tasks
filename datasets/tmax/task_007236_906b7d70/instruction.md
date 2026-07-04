You are acting as an artifact manager for a continuous integration system. We have received a custom binary archive file containing several build artifacts, but our standard tools cannot read it.

The archive is located at `/home/user/artifacts.bin`.

The file uses a custom binary format defined as follows:
1. **Magic Header**: The first 4 bytes are exactly `ARTF` (ASCII).
2. **Entry Count**: The next 4 bytes represent an unsigned 32-bit integer (little-endian) indicating the number of files in the archive.
3. **Entries**: The file entries immediately follow. Each entry consists of:
   - **Filename Length**: Unsigned 16-bit integer (little-endian).
   - **Filename**: UTF-8 string of the specified length.
   - **Compressed Size**: Unsigned 32-bit integer (little-endian).
   - **Original Size**: Unsigned 32-bit integer (little-endian).
   - **Compression Type**: Unsigned 8-bit integer (0 = Uncompressed, 1 = GZIP compressed).
   - **Data**: The file payload (length equals Compressed Size). If the Compression Type is 1, this payload is a standard GZIP stream.

Your task is to write a Go program at `/home/user/extractor.go` that reads `/home/user/artifacts.bin` and extracts **only** the shared library artifacts (files whose names end with `.so`). 

Requirements for your Go program:
- It must stream the file reads and writes (e.g., using `io.Reader` and `io.Copy`). Do not load the entire archive or the entire data payloads into memory all at once.
- It must parse the binary headers correctly.
- It must decompress the payloads if `Compression Type` is 1, or just copy them if it is 0.
- The matching `.so` files must be extracted and saved to the directory `/home/user/extracted/` with their original filenames.

Once you have written the program, execute it to perform the extraction. Create the `/home/user/extracted/` directory if it does not exist.