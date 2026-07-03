I am a researcher organizing some legacy datasets from an old sensor network. The data was recorded in a custom binary format by a logger that frequently raced with the writing process, sometimes resulting in interleaved or corrupted records.

I have a compiled binary parser for this format located at `/app/log_parser_oracle`, but the original C++ source code was lost. I need to port this to modern systems and integrate it into my pipeline, so I need a new C++ implementation that behaves **exactly** the same as the oracle.

Here is what I know about the binary file format:
1.  **Magic Header:** Every file starts with the 4 bytes `DAT\x00`.
2.  **Records:** The file contains a sequence of records. Each record has the following structure (all multi-byte integers are Little-Endian):
    *   `type` (1 byte): The record type.
        *   `0x10`: Int32 Data. Payload is a 4-byte signed integer.
        *   `0x11`: Int64 Data. Payload is an 8-byte signed integer.
        *   `0x30`: Multi-line Text Data. Payload is ASCII text.
    *   `timestamp` (8 bytes, uint64_t): Microseconds since epoch.
    *   `length` (2 bytes, uint16_t): The size of the payload in bytes.
    *   `payload` (`length` bytes): The actual data.
    *   `checksum` (1 byte): A simple XOR sum of the `type`, `timestamp` (8 bytes), `length` (2 bytes), and all bytes of the `payload`.

Output Format:
The oracle reads the binary file and produces a plain text file, writing one line per valid record.
Format per line: `<timestamp>|<TYPE_STRING>|<value>`
*   For Int32: `1623456789|INT32|-42`
*   For Int64: `1623456789|INT64|9000000000`
*   For Text: `1623456789|TEXT|<escaped_text>` (The oracle escapes literal backslashes as `\\` and literal newlines as `\n`).

**Important Error Handling (The "Race" Condition):**
Because of the logger race conditions, some records are corrupted.
If the calculated checksum for a record does NOT match the `checksum` byte at the end of the record, the oracle **silently drops** the record and attempts to find the next valid record. *However, because the `length` field might be corrupted, simply skipping `length` bytes after a bad checksum might not work.* You must reverse-engineer or observe how the oracle `/app/log_parser_oracle` recovers from checksum failures. (Hint: it scans forward byte-by-byte for a valid record type that leads to a correct checksum).

Your task:
1. Write a C++ program in `/home/user/my_parser.cpp`.
2. Compile it to `/home/user/my_parser`.
3. It must accept two arguments: `</path/to/input.bin> </path/to/output.txt>`.
4. Its output must be bit-for-bit identical to `/app/log_parser_oracle` for any valid, corrupted, or fuzzed input.

You can interact with `/app/log_parser_oracle` to test your assumptions about its recovery behavior.