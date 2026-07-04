You are an engineer building tools for an artifact manager that curates binary repositories. The repository logs its state changes in a custom Write-Ahead Log (WAL) format. We need a C++ utility that can parse this WAL format, process the log entries, and output the final state of the repository.

However, the documentation for this custom WAL format was partially lost, and the only record of the WAL magic header sequence is in an old schematic image located at `/app/schema.png`. 

Your task is to write a C++ program at `/home/user/wal_state_parser.cpp` and compile it to `/home/user/wal_state_parser` (using `g++ -O3 -lz wal_state_parser.cpp -o wal_state_parser`).

Here is the specification for the C++ program:
1. **Input:** The program must read from `stdin`. The input stream will be **gzip-compressed** binary data. You must use `zlib` to decompress the stream on the fly (e.g., by using `gzdopen(fileno(stdin), "rb")`).
2. **Magic Header:** The uncompressed stream starts with a 4-byte magic sequence. You must find out what this sequence is by reading the text from `/app/schema.png`. If the stream does not start with this exact 4-byte sequence, print `INVALID_MAGIC` to `stdout` and exit with status code `1`.
3. **Log Entries:** After the 4-byte magic header, the stream contains a sequence of binary commands until EOF. All multi-byte integers are Unsigned Little-Endian. The commands are:
   - **ADD (`0x0A`)**: Followed by a 2-byte Artifact ID and a 4-byte File Size. If the Artifact ID already exists in your state, ignore this command. Otherwise, add the artifact with the given size.
   - **REMOVE (`0x0B`)**: Followed by a 2-byte Artifact ID. If the Artifact ID exists, remove it from the state. If it doesn't exist, ignore this command.
   - **UPDATE (`0x0C`)**: Followed by a 2-byte Artifact ID and a 4-byte File Size. If the Artifact ID exists, update its size. If it doesn't exist, ignore this command.
4. **Output:** Once EOF is reached, print the final state to `stdout`. Print one line per active Artifact ID, sorted by ID in ascending order. The exact format for each line must be: `[ID] -> [Size] bytes` (e.g., `1024 -> 5000 bytes`). Exit with status code `0`.

Ensure your C++ program is highly robust against truncated entries (e.g., if a command is partially written at the end of the file, gracefully ignore the incomplete command and stop reading). 

You can use `tesseract` or any other pre-installed tools to analyze `/app/schema.png`. Write, compile, and thoroughly test your C++ program. Automated verification will randomly generate thousands of WAL streams and compare your compiled program's output byte-for-byte against a reference implementation.