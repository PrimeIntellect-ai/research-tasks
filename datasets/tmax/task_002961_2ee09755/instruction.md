You are acting as a backup administrator archiving log data from a fleet of microservices. We have a large directory of uncompressed logs in `/home/user/logs` consisting of JSON Lines (`.jsonl`) and CSV (`.csv`) files. Before these logs are shipped to cold storage, we need to extract only the critical errors and package them into fixed-size chunked files.

Your task is to create and run a Rust command-line application that accomplishes this.

Here are the requirements for your Rust application:
1. **Directory Traversal:** Recursively traverse the directory `/home/user/logs`.
2. **Streaming Parsing:** 
   - For `.jsonl` files: Read the file line-by-line. Parse the JSON. If the `"level"` field equals exactly `"CRITICAL"`, keep the record.
   - For `.csv` files: Read row-by-row (assume a header exists). If the `"status"` column equals exactly `"ERROR"`, keep the record as a JSON object mapping headers to values.
3. **Merging & Output Format:** 
   Convert all kept records into JSON lines. Each output line should be a JSON object with two keys:
   - `"source"`: the base name of the file it came from (e.g., `"app.jsonl"`).
   - `"data"`: the parsed JSON object of the record itself.
4. **Chunking & Atomic Writes:** 
   - Write the output to `/home/user/archive/`.
   - The output files must be named `archive_part_001.jsonl`, `archive_part_002.jsonl`, etc.
   - Each chunk must contain exactly 10 records, except potentially the last one.
   - To prevent downstream backup processes from reading incomplete files, you MUST use atomic writes: open a temporary file (e.g., `archive_part_XXX.jsonl.tmp`), write the 10 records, flush/close the file, and then rename it to the final `archive_part_XXX.jsonl` name.

Constraints:
- Initialize the Rust project in `/home/user/archiver`.
- You may use external crates like `serde`, `serde_json`, `csv`, and `walkdir`.
- Do not load entire files into memory; stream them.
- Once the code is written, compile it using `cargo build --release` and execute it to process the logs. Ensure `/home/user/archive/` is populated correctly.

Create the `/home/user/archive/` directory before running your program.