I have a messy directory of disorganized project files located at `/home/user/project_dump`. The files have lost their extensions, and some of them have been compressed using a custom Run-Length Encoding (RLE) format by a legacy archiving tool. 

I need you to write a Python script that recursively traverses `/home/user/project_dump`, identifies the file types based on their headers or contents, decompresses any custom RLE streams in memory on the fly, parses specific metadata from each file, and outputs a single JSON report at `/home/user/inventory.json`.

Here are the specifications for the file types and formats you will encounter:

**1. Custom RLE Compressed Files**
*   **Magic Header:** `CRLE` (4 bytes, ASCII)
*   **Format:** The remainder of the file consists of 2-byte pairs: `[count][byte]`. `count` is a 1-byte unsigned integer representing how many times the following `byte` should be repeated.
*   **Action:** Decompress the file stream in memory. The decompressed stream will be one of the three formats below. Analyze the decompressed stream exactly as if it were a regular file.

**2. ELF Binaries**
*   **Identifier:** Starts with `\x7fELF`
*   **Metadata to Extract:** The 64-bit Entry Point address. For the files in this directory, assume they are all 64-bit Little-Endian binaries. The 8-byte entry point address is located at offset `0x18` from the start of the file (or the start of the decompressed stream).
*   **Metric Format:** A hex string prefixed with `0x` (e.g., `"0x400000"`).

**3. SQLite Write-Ahead Logs (WAL)**
*   **Identifier:** Starts with the magic number `\x37\x7f\x06\x82` or `\x37\x7f\x06\x83`.
*   **Metadata to Extract:** The Page Size. This is a 32-bit Big-Endian unsigned integer located at offset `0x08`.
*   **Metric Format:** An integer (e.g., `4096`).

**4. GCode (3D Printing)**
*   **Identifier:** Starts with the exact ASCII string `; FLAVOR:Marlin`.
*   **Metadata to Extract:** The total number of linear move commands. Count the number of lines that start exactly with `G1 ` (G1 followed by a space).
*   **Metric Format:** An integer (e.g., `12`).

Your final output must be saved to `/home/user/inventory.json`. It must be a single JSON object where the keys are the **absolute paths** to the original files in `/home/user/project_dump`, and the values are objects with two keys: `"type"` (either `"ELF"`, `"WAL"`, or `"GCode"`) and `"metric"` (the extracted value described above).

Example Output Format:
```json
{
  "/home/user/project_dump/file_a": {
    "type": "ELF",
    "metric": "0x4005b0"
  },
  "/home/user/project_dump/sub/file_b": {
    "type": "WAL",
    "metric": 4096
  }
}
```

Please proceed to explore the directory, write the script, and generate the final JSON inventory.