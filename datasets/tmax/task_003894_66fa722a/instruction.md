You are helping a developer recover text data from a custom binary project archive format that has become corrupted with cyclic links. 

The developer has a binary file located at `/home/user/project_data.bin`. This file uses a custom format consisting of a sequence of records. Because the file generator had a bug, some internal links form infinite loops.

Your task is to write a C program that uses memory-mapped I/O (`mmap`) to parse this file, extract the text, and avoid infinite loops.

**Format Specification:**
Each record starts with a 5-byte header:
- **Byte 0**: Record Type. An ASCII character, either `T` (Text) or `L` (Link).
- **Bytes 1-4**: A 32-bit unsigned integer (little-endian). 
  - If the type is `T`, this integer represents the `Length` of the text payload immediately following the header.
  - If the type is `L`, this integer represents an absolute byte `Offset` from the beginning of the file where the next record is located. Link records do not have a payload.

**Parsing Rules:**
1. Start parsing at byte offset 0.
2. If you read a `T` record, extract its text payload and append it to your output, then continue parsing the very next byte immediately after the payload.
3. If you read an `L` record, immediately jump to the absolute byte offset specified in the header and continue parsing from there.
4. Keep track of the exact byte offsets of every record you visit. If you ever jump to or sequentially reach an offset you have *already visited*, you have detected an infinite loop. You must immediately stop parsing and exit gracefully.
5. If you reach the end of the file (EOF) or an offset beyond the file size, stop parsing.

Write your C code to `/home/user/parser.c`. Compile it and run it against `/home/user/project_data.bin`. 
The extracted text payloads must be concatenated in the exact order they were visited and written to `/home/user/extracted_text.txt`. Do not add any extra newlines or characters that are not in the `T` payloads.