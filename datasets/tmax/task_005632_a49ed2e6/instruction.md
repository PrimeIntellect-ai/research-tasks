You need to build a C++ configuration manager pipeline that processes a stream of configuration updates, handles multi-language text properly, deduplicates redundant changes, and computes rolling statistics.

You are given an input file at `/home/user/config_changes.jsonl`. Each line is a JSON object representing a configuration change event with the following fields:
- `id` (string): Unique identifier for the event.
- `ts` (integer): Unix timestamp of the event.
- `module` (string): The system module being configured.
- `key` (string): The configuration key.
- `value` (string): The new configuration value. This may contain complex Unicode text and escape sequences (e.g., `\uD83C\uDF0D`).

Write and execute a C++ program (using C++17 or later) that performs the following steps:

1. **Large-scale sorting:** Read all events from the input file and sort them chronologically by their `ts` (timestamp) in ascending order. If timestamps are identical, sort by `id` lexicographically.
2. **Hash-based deduplication:** Process the sorted events. A configuration update is considered a "duplicate" (and should be dropped) if the `value` is identical to the *most recently accepted* `value` for the exact same `module` and `key`. You must compute an `std::hash<std::string>` of the `value` (as a UTF-8 string) to verify this. (Initially, no keys have any values).
3. **Unicode processing & Pipeline logging:** For every event evaluated, write a log entry to `/home/user/pipeline.log`.
   - If accepted: `VALID: <id> - <module> - <byte_length_of_utf8_value>`
   - If dropped as duplicate: `DUPLICATE: <id>`
   *(Note: The byte length must be the exact number of bytes in the decoded UTF-8 string representation of the `value`, not the length of the escaped JSON string).*
4. **Rolling statistics computation:** For every *accepted* event, compute the rolling count of *accepted* events that occurred within the last 60 seconds (i.e., events with timestamp `T` where `current_ts - 60 <= T <= current_ts`). Write this to `/home/user/stats.csv` in the format:
   `id,rolling_count`

**Constraints & Instructions:**
- Use `g++` to compile your code. You may install standard development packages like `nlohmann-json3-dev` or `libssl-dev` using `apt-get` (sudo is not required if running as root, but you are the `user`, so use `sudo apt-get install -y ...` if needed).
- The final output files (`/home/user/pipeline.log` and `/home/user/stats.csv`) must be created exactly as specified.
- Your C++ source code should be saved as `/home/user/config_processor.cpp` and the compiled binary as `/home/user/config_processor`. Run it to produce the outputs.