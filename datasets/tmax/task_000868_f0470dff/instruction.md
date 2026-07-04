You are a data analyst setting up an automated data cleaning pipeline. You receive daily drops of CSV telemetry data, but some files contain malformed, anomalous, or malicious payloads in the text fields. You need to build a Rust-based filter tool and set up a cron schedule for it.

**Step 1: Video Reference Extraction**
We have a reference video clip located at `/app/reference.mp4`. 
Use `ffmpeg` to determine the exact total number of frames in this video. Let this integer be `F`. This value acts as an upper-bound configuration for our text processing limits.

**Step 2: Build the Rust CSV Filter**
Create a new Rust project at `/home/user/pipeline/`. Write a CLI application that streams a large CSV file from an input path, filters rows based on strict rules, and streams valid rows to an output path.
- **Entry point:** Compiled to `/home/user/pipeline/target/release/filter`
- **Usage:** `./filter <input_path.csv> <output_path.csv>`
- **CSV Structure:** The files contain four columns: `id,timestamp,user_agent,description`.
- **Processing & Streaming:** The program MUST process the files in a streaming fashion (e.g., using the `csv` crate) to handle files that are gigabytes in size without exhausting memory.
- **Tokenization & Normalization:** For the `description` column, tokenize the text by splitting on whitespace, and normalize it by converting all characters to lowercase.
- **Filtering Rules:** A row MUST BE DROPPED if either of the following is true:
  1. The normalized `description` contains the exact token `"eval"` or `"script"`.
  2. The total number of tokens in the `description` strictly exceeds `F` (the number of video frames extracted in Step 1).
- **Output:** The output CSV must include the header row and all rows that passed the filters, preserving their exact original text and formatting.

**Step 3: Pipeline Scheduling**
Write a bash script at `/home/user/setup_cron.sh` that, when executed, safely configures the user's crontab to schedule the following exact command:
`/home/user/pipeline/target/release/filter /var/data/incoming.csv /var/data/clean.csv`
This job must be scheduled to run exactly at the top of every hour (e.g., 00:00, 01:00, 02:00, etc.).

Ensure that your Rust binary is fully compiled in release mode before finishing.