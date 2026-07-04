You are an artifact manager responsible for curating binary repositories. We need to build a C++ utility to parse a stream of binary artifacts, but the curation rules depend on a secret corruption flag embedded in a video log.

### Step 1: Video Analysis
We have a video log of the curation feed at `/app/curation_log.mp4`. 
The video consists of completely black frames, except for exactly ONE frame which is completely RED (RGB: 255, 0, 0).
Find the 0-indexed frame number of this red frame. Let this number be `F`.

### Step 2: C++ Artifact Curator
Write a C++ program at `/home/user/repo_curator.cpp` and compile it to `/home/user/repo_curator`.
The program must read a binary stream from standard input (`stdin`) and write formatted text to standard output (`stdout`).

The stream consists of contiguous records. Each record has the following binary format (tightly packed, little-endian):
- **Magic bytes** (4 bytes): Must be exactly the ASCII string `ARTF`.
- **Size** (4 bytes): `uint32_t` representing the length of the data payload.
- **Flags** (2 bytes): `uint16_t` representing artifact properties.
- **Name** (16 bytes): ASCII string, padded with null bytes (`\0`) if shorter than 16 characters.
- **Data** (`Size` bytes): The raw artifact payload.

**Processing Rules:**
Read records sequentially until EOF. For each record:
1. If `Flags` exactly equals `F` (the frame number from Step 1), the artifact is completely corrupted. **Do not print anything** for this record.
2. Otherwise, if the least significant bit of `Flags` is 1 (`Flags & 0x01`), it is a valid artifact. Print: `[VALID] <Name> - <Size> bytes\n`
3. Otherwise, it is a disabled artifact. Print: `[IGNORED] <Name>\n`
*(Note: `<Name>` should only print up to the first null byte, or exactly 16 characters if no null byte is present).*

**Error Handling:**
Stop processing and print exactly the specified error message (followed by a newline) if any of these conditions are met:
- If a record's magic bytes are not `ARTF`, print `[ERROR] Invalid magic` and exit with code 1.
- If `Size > 1024`, print `[ERROR] Size too large` and exit with code 1.
- If standard input ends prematurely in the middle of a record (including payload), print `[ERROR] Incomplete record` and exit with code 1.
- If EOF is reached cleanly between records, exit gracefully with code 0.

Compile your program exactly at `/home/user/repo_curator`. Automated tests will rigorously fuzz your binary with random inputs to ensure it perfectly matches the reference parser.