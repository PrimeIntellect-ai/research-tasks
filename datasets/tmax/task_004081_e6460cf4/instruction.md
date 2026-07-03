You are tasked with implementing a C++ configuration manager utility that tracks configuration changes by parsing a custom binary Write-Ahead Log (WAL) stream.

We have received a specification for the WAL archive format as an image scan, located at `/app/wal_spec.png`. You must analyze this image (e.g., using `tesseract`) to understand the exact binary structure of the WAL headers and records. 

Your objective is to write a C++ program that:
1. Reads a binary WAL stream from `stdin` until EOF.
2. Validates the magic bytes and header format as specified in the image. If the stream is invalid, print exactly "INVALID FORMAT\n" to `stdout` and exit with code 1.
3. Iterates through all configuration change records (ADD, DEL, MOD operations) in the stream.
4. Maintains the running state of configuration keys (which are strings) and their values (which are strings).
5. Upon reaching the end of the stream, prints the final configuration state to `stdout`, one per line, sorted alphabetically by key, in the format `KEY:VALUE\n`. Exit with code 0.

Rules and Constraints:
- If a MOD operation targets a key that does not exist, ignore the operation.
- If an ADD operation targets a key that already exists, overwrite its value.
- If a DEL operation targets a non-existent key, ignore it.
- Your C++ source file must be saved at `/home/user/wal_tracker.cpp`.
- You must compile your program to `/home/user/wal_tracker` (e.g., `g++ -O2 /home/user/wal_tracker.cpp -o /home/user/wal_tracker`).

The automated verification system will test `/home/user/wal_tracker` against thousands of randomly generated WAL streams to ensure it is bit-exact equivalent to our reference implementation. Ensure your memory management is safe and your parsing strictly adheres to the binary lengths specified in the spec.