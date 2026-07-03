I am a technical writer trying to recover some lost documentation from a legacy wiki system. The only backup I have is a raw Write-Ahead Log (WAL) file located at `/home/user/wiki.wal`. 

I need you to write a C program that parses this WAL file, extracts the final content for each documentation entry, and exports it to a structured CSV file.

Here is the technical specification for the task:

1. **The WAL Format**:
   - The file consists of sequential binary records.
   - Each record has the following structure:
     - **Magic Bytes** (4 bytes): `0x44 0x4F 0x43 0x35` (ASCII for "DOC5")
     - **Document ID** (4 bytes): Unsigned 32-bit integer, little-endian.
     - **Payload Length** (4 bytes): Unsigned 32-bit integer, little-endian. This is the length of the compressed data segment in bytes.
     - **Compressed Data** (`Payload Length` bytes): The actual text of the document, compressed using a custom Run-Length Encoding (RLE).

2. **Custom RLE Compression**:
   - The compressed data consists of 2-byte pairs: `[Count][Character]`.
   - `Count` is a 1-byte unsigned integer (uint8_t) representing how many times the character repeats.
   - `Character` is a 1-byte ASCII character.
   - For example, the bytes `0x03 0x41 0x01 0x42` decompress to "AAAB".

3. **Log Navigation (The WAL aspect)**:
   - Because this is a transaction log, there may be multiple records for the same Document ID representing subsequent edits. 
   - You must only keep the **latest** (last appearing) version of the text for any given Document ID.

4. **Program Requirements**:
   - You must write your solution in C (`/home/user/extract.c`).
   - You **must** use Memory-Mapped I/O (`mmap`) to read the `/home/user/wiki.wal` file.
   - Compile it to `/home/user/extract` (e.g., using `gcc -O2 /home/user/extract.c -o /home/user/extract`).
   - The program must output the final extracted documents to `/home/user/docs.csv`.

5. **CSV Output Format**:
   - The output file `/home/user/docs.csv` must include a header: `DocID,Text`
   - Following the header, list the final text for each Document ID, sorted in ascending order by Document ID.
   - You can assume the decompressed text will only contain alphanumeric characters and spaces (no commas, quotes, or newlines), so no special CSV escaping is needed.

Please create the C program, compile it, and run it to produce the `docs.csv` file.