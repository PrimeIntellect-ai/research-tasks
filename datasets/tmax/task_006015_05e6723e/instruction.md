You are a localization engineer managing a time-series dataset of translation string updates. Your team previously used a naive bash pipeline to parse localization CSVs, but it was silently dropping records that contained embedded newlines in the translation strings. 

Your task is to build a robust, multi-stage data processing pipeline that safely fetches, validates, and processes these translation updates. You must use Rust to handle the CSV parsing and data normalization to ensure correctness.

Here are your specific requirements:

1. **Remote Data Fetching**:
   There is a local HTTP server running at `http://localhost:8080` hosting two CSV files: `data1.csv` and `data2.csv`. 
   Write a shell script `/home/user/pipeline.sh` that starts by downloading these files into the directory `/home/user/raw_data/`. 

2. **Validation Checkpoint**:
   In `pipeline.sh`, add a validation step after downloading that checks if both files were successfully downloaded and exist in `/home/user/raw_data/`. If either file is missing, the script should exit with an error.

3. **Data Processing (Rust)**:
   Create a new Rust project at `/home/user/l10n_cleaner`. Write a Rust program that reads all CSV files in `/home/user/raw_data/`. 
   - The CSV format is strictly: `timestamp,locale,msg_id,translation`.
   - The `translation` column is enclosed in double quotes and may contain embedded newlines (e.g., `\n`).
   - You must parse the CSV properly without dropping these multi-line rows.
   - **Normalization**: For the `translation` field, you must replace all newline characters (`\n` and `\r`) with a single space character (` `), and trim any leading or trailing whitespace.
   - Parse the `timestamp` as an integer.

4. **Time-Series Aggregation & Output**:
   The Rust program must combine the records from all CSVs, sort them chronologically in ascending order based on their `timestamp`, and write the results to a JSON Lines format file at `/home/user/clean_l10n.jsonl`.
   Each line in the output file must be a valid JSON object with the keys: `timestamp` (integer), `locale` (string), `msg_id` (string), and `translation` (string).

5. **Pipeline Orchestration**:
   Your `/home/user/pipeline.sh` script must orchestrate the entire flow:
   - Create directories if needed.
   - Fetch the data.
   - Validate the fetch.
   - Build the Rust project (e.g., using `cargo build --release`).
   - Run the compiled Rust binary to generate the `/home/user/clean_l10n.jsonl` file.

Ensure your Rust program handles dependencies correctly (e.g., using `csv` and `serde` crates in your `Cargo.toml`). Do not run the pipeline as root. When you are finished, execute your `/home/user/pipeline.sh` script to produce the final `clean_l10n.jsonl` file.