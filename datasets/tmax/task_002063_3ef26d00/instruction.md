You are a storage administrator managing disk space on a specialized print server. The server generates massive log files that occasionally embed archived, custom-compressed GCode files (3D printer instructions) inside multi-line log records.

Your task is to parse a specific log file, extract and decompress these GCode blocks, and archive the resulting files into a compressed tarball to free up disk space.

**Source Data:**
The log file is located at `/home/user/storage/server.log`. 

**Log Format:**
- The log contains standard timestamped server events.
- Embedded GCode files span multiple lines, delimited by start and end markers.
- Start marker: `=== BEGIN ARCHIVED GCODE: <filename> ===` (where `<filename>` is the name of the file).
- End marker: `=== END ARCHIVED GCODE ===`
- The lines between these markers contain the compressed GCode data.

**Custom Compression Algorithm:**
The GCode data inside the log has been encoded using a custom Hex-Run-Length-Encoding (Hex-RLE).
- The compressed payload is a continuous string of hexadecimal characters (split across multiple lines for log wrapping). You should ignore any whitespace or newlines in the payload.
- The format consists of consecutive 4-character hex chunks: `CCAA`.
- `CC` is a 2-character hex string representing the count (the number of times the character repeats).
- `AA` is a 2-character hex string representing the ASCII value of the character.
- Example: `03410142` means the character 'A' (hex 41) repeats 3 (hex 03) times, and 'B' (hex 42) repeats 1 (hex 01) time. Decompressed output: `AAAB`.

**Your Objectives:**
1. Create a directory `/home/user/extracted_gcode`.
2. Write a Python script to parse `/home/user/storage/server.log`, extract each embedded GCode block, decompress it using the Hex-RLE algorithm described above, and save it as a text file in `/home/user/extracted_gcode/` using the filename specified in the start marker.
3. Once extracted, use standard bash tools to create a compressed tarball of the directory at `/home/user/gcode_archive.tar.gz`.

Ensure your Python script runs successfully and creates the exact original GCode text in the extracted files.