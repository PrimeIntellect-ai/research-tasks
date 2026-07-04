You are tasked with organizing and normalizing a set of legacy project files. The previous developer left behind a directory of data files, but their format is inconsistent, and processing them requires using a legacy C library.

You have been provided with a compiled C shared library at `/home/user/libchecker.so`. This library exposes a single function:
`int check_magic(const char* filepath);`
This function takes an absolute or relative path to a file and returns `1` if the file has the correct proprietary magic header bytes, and `0` otherwise.

Your goal is to write a script (in Go, Python, or a language of your choice) to process the files located in `/home/user/legacy_data/`. 

Your script must satisfy the following requirements:
1. **Concurrency & Rate Limiting:** Process the files concurrently, but strictly limit the processing to exactly 2 concurrent workers at any given time to avoid overloading the legacy library.
2. **FFI:** Use Foreign Function Interface (FFI) (e.g., `cgo` in Go, or `ctypes` in Python) to invoke the `check_magic` function from `/home/user/libchecker.so` for each file.
3. **Encoding & Transformation:** For files where `check_magic` returns `1`:
   - Read the file.
   - Strip the first 4 bytes (the magic header).
   - The remainder of the file is a base64-encoded string. Decode this base64 payload.
   - The decoded bytes are encoded in `ISO-8859-1`. Convert these bytes to valid `UTF-8`.
   - Write the resulting UTF-8 text to `/home/user/organized_data/<filename>`.
   - Files where `check_magic` returns `0` should be completely ignored.
4. **Logging:** Keep track of the filenames of all successfully processed and converted files. Write these filenames (just the basenames, e.g., `file1.txt`), sorted alphabetically, one per line, to `/home/user/processed.log`.

Make sure to create `/home/user/organized_data/` before writing to it. You are responsible for any compilation or package installation your script requires.