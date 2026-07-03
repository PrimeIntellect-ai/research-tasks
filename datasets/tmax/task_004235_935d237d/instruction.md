You are tasked with building a configuration management parser that reconstructs the final state of a system based on a proprietary binary Write-Ahead Log (WAL) format. 

Another team has provided a specification for the WAL operations in an image file located at `/app/config_opcodes.png`. You will need to extract the exact OpCode byte values from this image (you can use `tesseract` to read it).

**System Specification:**
1. **The WAL File Format:**
   - Every WAL file starts with a 4-byte magic sequence: `CWAL`.
   - Following the magic sequence is a series of records.
   - Each record has the following binary layout:
     - `OpCode` (1 byte): Determines the operation type (refer to the image).
     - `Key Length` (2 bytes, little-endian): The length of the key string.
     - `Key` (ASCII string, length determined by the previous field).
     - If the OpCode is a type that requires a value (`OP_SET` or `OP_APPEND`):
       - `Value Length` (2 bytes, little-endian).
       - `Value` (ASCII string, length determined by the previous field).
     - If the OpCode is `OP_RM`, the `Value Length` and `Value` fields are omitted entirely.

2. **Configuration State Logic:**
   - The configuration manager maintains an internal state of Key-Value pairs (both are strings).
   - `OP_SET`: Sets the key to the provided value. If the key already exists, its value is overwritten.
   - `OP_RM`: Removes the key from the state. If the key does not exist, the operation is ignored.
   - `OP_APPEND`: Appends the provided value string to the end of the existing value for that key. If the key does not exist, it behaves identically to `OP_SET`.

3. **Output Format:**
   - After parsing the entire file, the program must print the final configuration state to standard output.
   - Print each key-value pair on a new line in alphabetical order by key.
   - Format: `[KEY] -> [VALUE]`
   - If the state is entirely empty, print nothing.

**Your Goal:**
Write a C++ program that reads a WAL file path as its first command-line argument, parses it, and prints the final state according to the rules above. 
Compile your program and save the executable to exactly `/home/user/wal_parser`.

*Note: You must handle arbitrary binary data gracefully and rely strictly on the field lengths, not null-terminators. Ignore trailing bytes if a record is incomplete or corrupted at the end of the file (stop parsing cleanly).*