You are tasked with implementing the ingestion pipeline for a secure configuration management system. You need to write a C++ program that validates, normalizes, and safely stores incoming configuration updates.

The configuration updates are stored as JSON files. However, our legacy upstream systems sometimes send these files in UTF-16LE encoding instead of UTF-8. Furthermore, we receive malicious configuration payloads that attempt path traversal attacks or lack proper authorization.

Your objective is to write a C++ program at `/home/user/ingest.cpp` and compile it to `/home/user/ingest`.

Requirements for `/home/user/ingest`:
1. **Command Line Interface:** The program must accept exactly two arguments: `./ingest <input_config_file> <output_directory>`
2. **Encoding Conversion:** The program must read the input file. If the file starts with a UTF-16LE Byte Order Mark (BOM) `FF FE` or is otherwise UTF-16LE encoded, it must accurately convert the contents to UTF-8 before parsing.
3. **JSON Parsing:** Parse the UTF-8 payload. A single-header JSON library is provided for you at `/app/include/json.hpp` (nlohmann/json).
4. **Validation (Adversarial Filtering):**
   - The JSON object must contain an `"auth_token"` string field.
   - The value of `"auth_token"` must exactly match the spoken passphrase found in the audio file located at `/app/auth_token.wav`. You will need to transcribe this audio file to find the required token.
   - The JSON object must contain a `"target_path"` string field.
   - The `"target_path"` must NOT contain any directory traversal sequences (i.e., the substring `..` is strictly forbidden).
   - If any validation fails, the input is malformed, or the file does not exist, your program must exit with a non-zero exit code (e.g., `return 1;`) and must NOT write any output.
5. **Atomic Write (Safe Storage):** If the configuration is perfectly valid, your program must write the parsed JSON (pretty-printed with 4 spaces) to `<output_directory>/<basename_of_input_file>`. To prevent partial reads by other system components, this write MUST be atomic: write the data to a temporary file in the same output directory first, and then use the POSIX `rename()` system call (or `std::filesystem::rename`) to move it to the final destination path.
6. **Success:** Return exit code `0` on successful validation and write.

To help you develop and test your program, we have provided two testing corpora:
- `/app/corpus/clean/`: Contains valid configuration files (in both UTF-8 and UTF-16LE) that your program MUST successfully process (exit 0 and output the file).
- `/app/corpus/evil/`: Contains malformed, unauthorized, or malicious configuration files that your program MUST reject (exit non-zero, no output).

Please write, compile, and thoroughly test your C++ program against the corpora. Ensure you extract the correct `auth_token` from the audio file to pass the authorization check.