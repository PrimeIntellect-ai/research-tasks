You are assisting a technical writer in organizing documentation logs. The writer has provided a screencast video of their workflow, which interestingly contains an embedded executable acting as a reference implementation for a log parsing tool.

Your objective has two parts:

1. **Extract the Reference Tool**:
   The video file is located at `/app/screencast.mp4`. 
   Use `ffmpeg` to extract the attached file named `oracle_tracker` from this video. 
   Save it to `/home/user/oracle_tracker` and ensure it has executable permissions. This is the reference binary you must replicate.

2. **Develop the C++ Log Parser**:
   Write a C++ program at `/home/user/doc_tracker.cpp` and compile it to `/home/user/doc_tracker`.
   This program must parse file-watcher event logs from standard input and output the final directory state as a minified JSON string to standard output.

   **Input Format**:
   A stream of lines (separated by `\n`). Each line represents a file event:
   `[TIMESTAMP] ACTION /path/to/file SIZE`
   - `TIMESTAMP`: Integer.
   - `ACTION`: Can be `CREATE`, `MODIFY`, or `DELETE`.
   - `PATH`: Absolute path containing alphanumeric characters and `/`.
   - `SIZE`: Integer representing file size in bytes.

   **Output Format**:
   A minified JSON object representing the final directory tree. 
   - Directories are nested JSON objects.
   - Files are represented by their integer size.
   - If a file is deleted, it must be removed from the JSON.
   - If a directory is emptied (all files deleted), it should remain as an empty JSON object `{}`.
   - Ignore events on paths that don't start with `/`.

   *Example Input*:
   ```
   [1] CREATE /docs/readme.md 500
   [2] CREATE /docs/api/v1.md 1200
   [3] MODIFY /docs/readme.md 550
   [4] DELETE /docs/api/v1.md 0
   ```

   *Example Output*:
   ```json
   {"docs":{"api":{},"readme.md":550}}
   ```

Your C++ code should ideally use modern C++ (C++17/20). You may install JSON libraries (like `nlohmann-json3-dev`) via `apt` if needed. Your compiled executable must exactly match the behavior and output of the `oracle_tracker` on any valid sequence of events.