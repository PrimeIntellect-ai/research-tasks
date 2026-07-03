You are tasked with replacing a legacy proprietary configuration tracking daemon with a modern, maintainable C++ implementation. 

We have a stripped legacy binary located at `/app/legacy_config_tracker`. It is a configuration manager that tracks state changes. 

Here is what we know about how it works:
1. **Invocation**: It is invoked as `/app/legacy_config_tracker <baseline_config_file>`.
2. **Baseline Config (Memory-Mapped)**: The baseline config is a custom binary file format. It starts with a 4-byte magic header `CFG1`. This is followed by a sequence of key-value records: `[2-byte unsigned little-endian key length][key bytes][4-byte unsigned little-endian value length][value bytes]`. You must use memory-mapped I/O (`mmap`) to load this file efficiently.
3. **Streaming Deltas (JSON)**: Once initialized, the program streams JSON lines from `stdin`. Each line is a JSON object representing a configuration change event: `{"op": "PUT", "k": "key_name", "v": "value_string"}` or `{"op": "DEL", "k": "key_name"}`. You must parse this structured JSON data and update the active configuration state in memory.
4. **File Watching**: Concurrently, the program watches the `<baseline_config_file>` on disk. If the file is modified externally, the program detects the change (using `inotify`), re-mmaps the file, and resets its internal state to exactly match the new baseline file, discarding any streaming deltas received up to that point.
5. **Manifest Generation**: After processing *each* JSON event from `stdin` OR after *each* file watch reload, the program prints a single line to `stdout` containing the lowercase SHA256 checksum of the entire active configuration state. 

Your goal is to write a C++ program at `/home/user/config_tracker` that behaves exactly identically (BIT-EXACT) to `/app/legacy_config_tracker`.

**Notes for your implementation:**
* You have access to the legacy binary. Use tools like `strings`, `strace`, `ltrace`, or a hex editor to reverse-engineer any missing details, such as exactly how the configuration state is serialized before hashing (e.g., sorting order, delimiters).
* You must implement the file watching mechanism correctly using Linux primitives (`inotify`).
* Ensure you handle edge cases the same way the oracle does (e.g., deleting a non-existent key, malformed JSON, etc., by observing the oracle's output).
* Compile your final solution to `/home/user/config_tracker`. It must be a standalone executable. Use `-lcrypto` for SHA256 and any JSON library available in the environment (e.g., `nlohmann/json.hpp` which you can install or download).