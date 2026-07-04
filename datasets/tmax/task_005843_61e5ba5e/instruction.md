I need you to help me organize some noisy project logs into a more structured format. Currently, a background process dumps everything into a single JSON Lines (JSONL) file. Because this file is constantly written to and could be rotated at any time, we need a robust tool to process it via standard input.

Your task is to write a Rust CLI application that reads JSONL logs from standard input, transforms them, and organizes them into separate CSV files based on the source module. Additionally, it must securely maintain a summary file using atomic writes.

Here are the requirements:
1. Create a Rust project (or standalone script compiled with `rustc`) located at `/home/user/log_transformer`.
2. The program must read line-by-line from `stdin`.
3. Each input line is a JSON object with the following fields: `timestamp`, `module`, `level`, and `message`.
4. For each line, append the data to a CSV file named `/home/user/organized_logs/<module>.csv`. The CSV should not have a header row and should be formatted strictly as: `timestamp,level,message`. 
5. The program must maintain a count of processed logs per module and write this to `/home/user/organized_logs/summary.json` formatted as a simple JSON object (e.g., `{"api": 5, "db": 2}`). 
6. **Crucial:** Because the script might be interrupted during processing, you must update `summary.json` safely using atomic writes. Every time the summary is updated, write the new JSON to `/home/user/organized_logs/summary.json.tmp` and then rename it to `/home/user/organized_logs/summary.json`.
7. Once your Rust program is written and compiled to an executable at `/home/user/log_transformer_bin`, execute it by piping the contents of `/home/user/raw_logs.jsonl` into it.

Please write the Rust code, compile it, and process the logs. Ensure all files end up in `/home/user/organized_logs/` which you should create if it doesn't exist.