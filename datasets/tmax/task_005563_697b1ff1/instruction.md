A background configuration manager on our server dumps state changes to a custom hybrid binary/text log file at `/home/user/config.binlog`. Recently, a poorly timed log rotation script raced with the writer process, leaving the active log file truncated. 

Your task is to write a C++ program at `/home/user/recover.cpp` that reads this custom binary log, parses out the valid multi-line configuration payloads, cleanly handles the truncated final record, and exports the recovered configurations into a JSON file at `/home/user/recovered_configs.json`.

Here are the specifications for the `config.binlog` file format:
1. The file consists of a sequence of records.
2. Each record begins with a 12-byte binary header:
   - `Magic`: 4 bytes, ASCII string "CFG1"
   - `Timestamp`: 4 bytes, unsigned 32-bit integer (little-endian) representing the UNIX epoch time.
   - `Length`: 4 bytes, unsigned 32-bit integer (little-endian) representing the size of the text payload in bytes.
3. Immediately following the header is the multi-line text payload of exactly `Length` bytes.
4. Due to the log rotation race condition, the *last* record in the file is truncated. This means either the header is incomplete, or the remaining bytes in the file are less than the `Length` specified in the header. Your program must detect this EOF/truncation condition and gracefully discard the partial record without crashing.

Your C++ program must:
1. Parse `/home/user/config.binlog`.
2. Extract the text payloads of all *complete, valid* records.
3. Convert these payloads into a JSON string array and write it to `/home/user/recovered_configs.json`. The output must be valid JSON matching this exact structure:
```json
[
  "payload 1 text...",
  "payload 2 text..."
]
```
Note: Ensure you escape newlines and quotes properly when generating the JSON array.

Compile your program (e.g., using `g++ -std=c++17 /home/user/recover.cpp -o /home/user/recover`) and run it to produce the final JSON file.