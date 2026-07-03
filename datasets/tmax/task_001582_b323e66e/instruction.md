You are tasked with building a robust intake filter for a legacy configuration management system. 

Our fleet of servers uploads their state using a proprietary multi-part archive format called `.cpack`. We have a legacy, stripped compiled binary located at `/app/chunk_decoder` that handles the custom decompression of individual payload blocks. However, this binary is fragile: it crashes or executes arbitrary code if fed maliciously crafted compressed data, and it has no concept of file paths or safety.

We are under attack by malicious nodes sending crafted `.cpack` archives. Your job is to write a Rust command-line tool that acts as a secure front-end parser and sanitizer.

**The `.cpack` Format Details:**
A `.cpack` file contains one or more sequential entries. There is no global header. Each entry consists of:
1.  **Magic Bytes:** 4 bytes, exactly `CPCK`.
2.  **Filename Length (`L`):** 2 bytes, little-endian unsigned integer.
3.  **Filename:** `L` bytes, encoded in **Windows-1252** (you must correctly decode this to UTF-8).
4.  **Payload Length (`D`):** 4 bytes, little-endian unsigned integer.
5.  **Payload:** `D` bytes of compressed binary data.

**Requirements for your Rust tool (`/home/user/sanitizer`):**
1.  Initialize a new Rust project at `/home/user/sanitizer`. Your final executable must be runnable via `cargo run --release -- <file_path>`.
2.  Open the file and immediately acquire a **shared file lock** (`flock`) on it to prevent concurrent writers from modifying it while you read.
3.  Iterate through all entries in the file sequentially until EOF.
4.  **Sanitization Checks:** For each entry, you must reject the file if:
    *   The magic bytes are incorrect or missing. (Print `REJECT: BAD MAGIC`)
    *   The decoded filename contains directory traversal sequences (`../` or `..\`) or is an absolute path (starts with `/` or `\`). (Print `REJECT: TRAVERSAL`)
    *   The payload length `D` exceeds 10,485,760 bytes (10MB) to prevent decompression bombs. (Print `REJECT: TOO LARGE`)
5.  **Decompression Validation:** If the entry passes the checks above, extract the `D` bytes of payload and pipe them exactly to the standard input of `/app/chunk_decoder`. 
    *   If `/app/chunk_decoder` exits with a non-zero status code or is killed by a signal, print `REJECT: DECODER CRASH` and immediately exit.
6.  If the entire file is parsed successfully and all payloads decompress correctly, print `ACCEPT` and exit with status `0`.
7.  Any rejection must exit with status `1`.

**Testing Your Tool:**
We have provided two corpora of `.cpack` files:
*   `/home/user/corpora/clean/`: Contains valid configuration archives. Your tool MUST print `ACCEPT` and exit 0 for all of these.
*   `/home/user/corpora/evil/`: Contains malicious archives (directory traversals, zip bombs, invalid encodings, decoder crash payloads). Your tool MUST print a `REJECT: ...` message and exit 1 for all of these.

Ensure your Rust code handles file I/O efficiently and does not load entire payloads into memory unless necessary. Use standard Rust crates (e.g., `encoding_rs` for Windows-1252, `fs4` or `rustix` for locking) by adding them to your `Cargo.toml`.