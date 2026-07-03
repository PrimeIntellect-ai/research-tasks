You are a storage administrator responsible for managing disk space on a distributed logging cluster. The system is currently running out of space due to corrupted, malicious log blobs being written by an upstream service. 

Your objective is to write a C++ sanitization and compression tool that filters out these malicious logs, compresses the valid ones using a custom algorithm, and integrate this tool into our logging pipeline. 

### Infrastructure
There are three services running in the background (already started via `/app/startup.sh`):
1. **Frontend Receiver**: A Python service on port 8080 that receives binary log chunks.
2. **Log Queue**: A Redis instance on port 6379.
3. **Archiver**: A bash script `/app/archiver.sh` that pulls from Redis, saves to disk in `/home/user/logs/raw/`, and deletes the queue.

### Task Requirements

**Part 1: The C++ Sanitizer**
Write a C++ program at `/home/user/sanitizer.cpp` (and compile it to `/home/user/sanitizer`) that takes two arguments: an input file path and an output file path.
`./sanitizer <input_bin> <output_zarc>`

The input is a custom binary log file containing consecutive records. Each record has:
- **Header**: 4 bytes Magic Number (`0xDEADBEEF`), followed by 4 bytes Unsigned Integer (Little Endian) representing `Payload_Size`.
- **Payload**: `Payload_Size` bytes of UTF-8 multi-line log text.

Your tool must parse these records. A record is **MALICIOUS** (and must be completely dropped) if:
- The multi-line text payload contains the string `STATUS: FATAL_BLOAT` on its *second* line.
- OR the payload contains the exact substring `[CORRUPT]`.

For all **VALID** (clean) records, your tool must apply a custom Run-Length Encoding (RLE) compression to the payload. 
*Custom RLE rule*: Any character repeated 3 or more consecutive times should be replaced by `~[char][count]`. (e.g., `AAAAA` becomes `~A5`).

The output file must be a custom archive format (`.zarc`):
- Start with a global header: `ZARC001\n`
- For each valid compressed record, append: `[Original Payload Size as 4-byte LE][Compressed Size as 4-byte LE][Compressed Payload]`

**Part 2: Integration**
Modify `/app/archiver.sh` so that instead of just dumping raw files from Redis to `/home/user/logs/raw/`, it pipes the dumped binary file through your `/home/user/sanitizer`, saves the output to `/home/user/logs/archive/<timestamp>.zarc`, and deletes the raw dump.

**Part 3: Batch Verification Log**
There are two directories containing historical test logs:
- `/home/user/corpus/clean/` (contains 50 valid `.bin` files)
- `/home/user/corpus/evil/` (contains 50 malicious `.bin` files)

Write a bash script `/home/user/verify.sh` that loops over both directories, runs your sanitizer on each file (outputting to `/dev/null` or a temp file), and logs the exit code and whether it produced any valid records. However, for automated testing, we will run our own verification harness directly against your compiled `/home/user/sanitizer`.

Ensure your C++ code compiles successfully with `g++ -O3 -std=c++17` and that the services are properly reconfigured.