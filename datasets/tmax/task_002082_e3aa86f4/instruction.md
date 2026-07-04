You are a localization engineer managing translation feedback from three regional teams: US, Germany (DE), and Japan (JP). Each team provides a daily feedback log, but they use different character encodings and timestamp formats.

You must write a Rust program located in `/home/user/loc_pipeline` that implements a data processing pipeline to normalize and merge these files.

**Input Files (already existing on the system):**
1. `/home/user/inputs/us_feedback.csv`
   - Encoding: UTF-8
   - Format: `MM/DD/YYYY HH:MM:SS AM/PM,key,comment`
   - Timezone: UTC-8 (Fixed offset)
2. `/home/user/inputs/de_feedback.csv`
   - Encoding: ISO-8859-1
   - Format: `DD.MM.YYYY HH:MM:SS,key,comment`
   - Timezone: UTC+1 (Fixed offset)
3. `/home/user/inputs/jp_feedback.csv`
   - Encoding: Shift_JIS
   - Format: `YYYY/MM/DD HH:MM:SS,key,comment`
   - Timezone: UTC+9 (Fixed offset)

**Requirements for your Rust Pipeline:**
Your Rust program must be an orchestrator that executes a 3-stage Directed Acyclic Graph (DAG) pipeline. It must sequentially execute these steps and create the corresponding intermediate files to prove the DAG execution flow:

*   **Phase 1: Decode.** Read each input file, decode it to standard UTF-8, and save the intermediate outputs to `/home/user/temp/decoded_us.csv`, `/home/user/temp/decoded_de.csv`, and `/home/user/temp/decoded_jp.csv`.
*   **Phase 2: Align Timestamps.** Read the decoded CSVs, parse the timestamps according to their specific formats and timezones, convert them to UTC in standard ISO 8601 format (e.g., `2024-01-01T15:00:00Z`), and write the updated rows to `/home/user/temp/aligned_us.csv`, `/home/user/temp/aligned_de.csv`, and `/home/user/temp/aligned_jp.csv`.
*   **Phase 3: Merge.** Read the three aligned CSVs, merge all rows into a single list, sort them chronologically (oldest to newest) based on the UTC timestamp, and output them as a single JSON array to `/home/user/final_output.json`.

**JSON Output Format:**
The final JSON file must strictly be an array of objects, minified (no extra whitespace), with the following keys:
`[{"timestamp":"YYYY-MM-DDTHH:MM:SSZ","key":"translation_key","comment":"translated_text"}]`

*   Use `cargo new loc_pipeline` in `/home/user/` to start.
*   You may use standard Rust crates (e.g., `chrono`, `encoding_rs`, `csv`, `serde`, `serde_json`).
*   Create the `/home/user/temp` directory if it does not exist.
*   Build and run your pipeline to produce the final output.