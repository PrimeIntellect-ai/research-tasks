You are an artifact manager responsible for curating a binary repository. You have received a raw system log and a directory of newly uploaded ELF binary artifacts. Your goal is to identify the valid artifacts from the log, parse their binary headers to extract architecture information, and generate a structured JSON Lines (JSONL) report.

Here are the specific requirements:

1. **Text Transformation:**
   You have a raw log file located at `/home/user/artifact_log.txt`. Many lines are debug noise, but valid artifact validation requests start exactly with the string `VALIDATE: ` followed by the artifact's filename (e.g., `VALIDATE: target_bin`).
   Use command-line text processing tools (like `sed`, `awk`, or `grep`) to extract just the filenames of these valid artifacts and save them to `/home/user/target_files.txt` (one filename per line).

2. **ELF Parsing in Rust:**
   The actual artifact binaries are stored in the `/home/user/artifacts/` directory. 
   Create a new Rust Cargo project in `/home/user/elf_inspector`. Write a Rust CLI tool that takes the full path to an ELF file as its first argument. 
   Using the `goblin` crate (you may add it to your `Cargo.toml`), parse the ELF header of the provided file and extract two specific fields:
   - The architecture machine ID (`e_machine`)
   - The entry point address (`e_entry`)

3. **Format Conversion & Reporting:**
   For each file parsed, your Rust tool must print exactly one line of JSON to standard output in the following format:
   `{"file": "<basename_of_file>", "machine": <integer_machine_id>, "entry": <integer_entry_point>}`
   *(Note: The `entry` value should be output as a standard base-10 integer, not hex).*

4. **Execution:**
   Write a short shell loop that reads each filename from `/home/user/target_files.txt`, runs your Rust tool on the corresponding file in `/home/user/artifacts/`, and appends the JSON output to `/home/user/final_report.jsonl`.

When you are finished, the file `/home/user/final_report.jsonl` should contain the metadata for all valid artifacts listed in the log.