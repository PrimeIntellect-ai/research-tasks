You are helping a technical writer build a live documentation aggregator. They receive continuous updates from different engineering teams in the form of multi-line log snippets dropped into a specific directory. You need to write a Rust tool that monitors this directory, parses the multi-line documentation records, and safely transforms them into a structured binary archive file.

Here is the complete specification for the task:

1. **Environment & Paths**:
   - Work directory: `/home/user/workspace` (Create your Rust project here).
   - Watch directory: `/home/user/doc_watch` (Create this directory. The tool must watch it for changes).
   - Output archive: `/home/user/doc_archive.bin` (The tool will create and append to this binary file).

2. **Input Format (Multi-line parsing)**:
   The files dropped into the watch directory will contain text with multi-line records. Each record starts with a header, contains body text, and ends with a footer. Extraneous text outside these blocks must be ignored.
   Format:
   ```
   >>>DOC: [Title]
   [Body Line 1]
   [Body Line N]
   <<<END
   ```
   *Example*:
   ```
   Ignored text here...
   >>>DOC: API V2 Endpoint
   This endpoint allows fetching user details.
   Rate limit: 100/min.
   <<<END
   More ignored text...
   ```

3. **Output Format (Binary Writing)**:
   Whenever a valid record is parsed, it must be appended to `/home/user/doc_archive.bin`.
   The binary format for **each record** must be exactly:
   - Magic bytes: `DOC1` (4 bytes: `0x44 0x4F 0x43 0x31`)
   - Title length: 1 byte (u8)
   - Title bytes (UTF-8, exactly 'Title length' bytes)
   - Content length: 4 bytes (u32, **Little Endian**)
   - Content bytes (UTF-8, exact content between the header and footer, including newlines but excluding the header/footer lines themselves).

4. **File Locking**:
   Because multiple instances of the aggregator or other processes might access the archive, your Rust program **must** acquire an exclusive file lock (using a library like `fs2` or `fs4`, or standard POSIX locking) on `/home/user/doc_archive.bin` before appending a parsed record, and release it immediately after writing.

5. **File Watching**:
   The tool must continuously watch `/home/user/doc_watch` for modified or newly created files (e.g., using the `notify` crate) and process any new records appended to them. Keep track of file sizes or simply re-parse new incoming files. For simplicity, assume files are written once completely and then moved/created in the directory, so you can just parse the whole file upon a `Create` or `Modify` event.

6. **Deliverables**:
   - Write the complete Rust project in `/home/user/workspace/doc_aggregator`.
   - Compile the project in release mode.
   - Copy the final executable to `/home/user/doc_daemon`.
   - Ensure the executable is statically linked or runs in the current environment without missing shared libraries.

To complete the task, build the application, leave the binary at `/home/user/doc_daemon`, and exit. Our automated test will start your daemon, write simulated logs to the watch directory, and verify the resulting binary archive.