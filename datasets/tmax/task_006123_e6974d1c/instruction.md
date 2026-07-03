You are acting as a storage administrator managing disk space and system security. We have a system that archives old multi-line application logs using a proprietary custom archive format called "SLOG" to save space. Recently, we suspect a compromised service has been writing malicious archives attempting to overwrite system files via path traversal (a "Zip Slip" attack). 

Your task is to write a C++ program that safely extracts these archives, and then parse the extracted logs to identify critical disk space errors.

**Phase 1: Configuration**
Your program must read a configuration file located at `/home/user/slog_config.ini`. It will contain two lines:
```ini
extract_dir=/home/user/extracted
quarantine_log=/home/user/quarantine.log
```
Your program must create the `extract_dir` if it does not exist.

**Phase 2: Extraction and Decompression**
Write a C++ program (e.g., `/home/user/extractor.cpp`) and compile it. The program must process the archive located at `/home/user/server_logs.slog`.

The `.slog` binary format is defined as follows:
1. **Magic Header:** 4 bytes ASCII `SLOG`.
2. **File Count:** 4 bytes, unsigned 32-bit integer, little-endian.
3. **File Entries** (repeated File Count times):
   - **Filename Length:** 2 bytes, unsigned 16-bit integer, little-endian.
   - **Filename:** ASCII string of the specified length.
   - **Data Stream:** The file's data is compressed using a custom Run-Length Encoding (RLE). The stream consists of pairs of bytes: `[count][character]`. `count` is an unsigned 8-bit integer representing how many times the `character` (1 byte) is repeated. If `count` is `0`, it marks the end of the file's data stream (the `character` byte for a count of 0 is undefined and should be ignored, but is present to keep the 2-byte alignment; typically it's just `0x00`).

*Security Requirement (Zip Slip Prevention):*
Before extracting a file, check its filename. If the filename starts with `/` (absolute path) or contains `../` (parent directory traversal), **do not extract it**. Instead, append the malicious filename on a new line to the file specified by `quarantine_log` in the config.

Valid files should be decompressed and written to the `extract_dir`.

**Phase 3: Multi-line Log Parsing**
The extracted files are text files containing multi-line logs. A new log entry always starts with a timestamp enclosed in brackets, e.g., `[2023-10-25 14:00:00]`. An entry continues across multiple lines until the next `[` at the beginning of a line, or the end of the file.

Using a script or extending your C++ program, parse all successfully extracted `.txt` files in the `extract_dir`. Find all complete multi-line log entries that contain the string `CRITICAL_SPACE_ERROR`. Append these complete multi-line entries (exactly as they appeared in the extracted files) to `/home/user/critical_errors.txt`. Separate each matched multi-line entry with a blank line.

To begin, the archive `/home/user/server_logs.slog` and config `/home/user/slog_config.ini` are already present on the system.