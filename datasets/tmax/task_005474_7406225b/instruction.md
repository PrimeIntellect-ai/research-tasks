You are an AI assistant helping a DevOps engineer build an artifact manager for a curated binary repository. 

Our system receives large artifact files split into multiple chunks and compressed using a proprietary (but simple) custom encryption/compression. These chunks are delivered as `.part` files. Additionally, the archives contain symlink definitions to recreate the necessary directory structures. 

However, we recently had an incident where a generated archive contained cyclic symlinks (an infinite loop), causing our backup scripts to crash. We also run the extraction of these `.part` files completely in parallel to save time, which currently causes file corruption because multiple processes try to write chunks to the same destination file simultaneously.

Your task is to write a C++ program `/home/user/art_tool.cpp` and compile it to `/home/user/art_tool`. 

**The C++ program must:**
1. Accept exactly one argument: the path to a `.part` file.
2. Read and parse the custom binary archive format (detailed below).
3. Extract file chunks:
   - "Decompress" them by XOR-ing every byte of the chunk data with the hex value `0xAA`.
   - Write the chunk to the correct destination file inside `/home/user/out_files/`.
   - **Crucial:** Because `art_tool` will be executed on multiple `.part` files concurrently in the background by our test suite, you **must** use POSIX file locking (`fcntl` or `flock` exclusive locks) when opening, writing, and closing the destination files to prevent race conditions. Ensure the file is opened in a way that allows writing to specific offsets without truncating existing data written by other processes.
4. Extract symlinks:
   - Create the symlink inside `/home/user/out_files/`.
   - **Crucial:** Before creating a symlink, evaluate if it creates an infinite cycle (e.g., A -> B, B -> C, C -> A). You must check the current state of `/home/user/out_files/` to see if creating this link would form a loop. If a cycle is detected, DO NOT create the symlink. Instead, append the name of the symlink (just the base name) to `/home/user/cycle_log.txt`.

**Archive Format Specification (.part files):**
All multi-byte integers are in Little Endian format.
- **Header:** 4 bytes magic string: `ART\0`
- **Entries:** Following the header are 0 or more entries. Each entry consists of:
  - `uint8_t type`: `0` for File Chunk, `1` for Symlink.
  - `uint16_t path_len`: Length of the destination path string.
  - `char path[path_len]`: The relative path of the file/symlink (e.g., `bin/app`).
  - **If type == 0 (File Chunk):**
    - `uint32_t offset`: The exact byte offset where this chunk should be written in the destination file.
    - `uint32_t chunk_size`: The size of the chunk data.
    - `char chunk_data[chunk_size]`: The XOR-encoded data.
  - **If type == 1 (Symlink):**
    - `uint16_t target_len`: Length of the target path string.
    - `char target[target_len]`: The target of the symlink.

**Setup Instructions:**
- The `.part` files are located in `/home/user/repo/`.
- Ensure `/home/user/out_files/` exists.
- Write your code, compile it using `g++ -O2 -std=c++17 /home/user/art_tool.cpp -o /home/user/art_tool`.
- Run your tool sequentially on all files in `/home/user/repo/` to ensure it works. 
- (During automated testing, we will run `for f in /home/user/repo/*.part; do /home/user/art_tool "$f" & done; wait` to verify your file locking logic).

When you are finished, ensure the compiled `/home/user/art_tool` exists, all files have been extracted to `/home/user/out_files/`, and any detected cycles are logged in `/home/user/cycle_log.txt`.