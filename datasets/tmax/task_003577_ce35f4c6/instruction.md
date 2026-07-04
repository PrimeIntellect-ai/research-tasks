You are a data scientist tasked with building a robust data cleaning pipeline for IoT sensor data. We had a reference implementation for cleaning our JSON-lines logs, but the source code was lost. We only have a stripped compiled binary remaining at `/app/oracle_cleaner`. 

Your goal is to reverse-engineer the logic, write a new Rust implementation from scratch, and build an ingestion pipeline. 

Here are the requirements:

1. **Understand the constraints:** The lead engineer left a voice memo at `/app/schema_rules.wav` detailing the schema validation rules for the dataset. You must transcribe or listen to this audio to extract the exact constraints for filtering records.
2. **Build the Rust Cleaner:** 
   Create a new Rust project at `/home/user/cleaner`.
   Write a Rust CLI tool that reads a JSON-lines stream from `stdin` and writes the cleaned JSON-lines to `stdout`.
   - It must parse each line as JSON. The expected fields are `device_id` (string), `temperature` (number), and `notes` (string).
   - It must drop any JSON record that violates the schema constraints mentioned in the audio file.
   - **Crucial fix:** The `notes` field contains unicode escape sequences (e.g., `\uXXXX`). You must decode these to their actual UTF-8 characters. If an escape sequence is invalid (e.g., invalid hex or un-paired surrogate), replace the entire invalid escape sequence with the Unicode Replacement Character (`U+FFFD`).
   - The output must be valid, minified JSON-lines.
   - Your compiled binary (`/home/user/cleaner/target/release/cleaner`) must be **bit-exact equivalent** to the behavior of `/app/oracle_cleaner` for *any* arbitrary JSON-lines input. Our automated CI will aggressively fuzz your binary against the oracle with thousands of random inputs.
3. **Orchestrate the ETL Pipeline:**
   Write a bash script at `/home/user/pipeline.sh` that implements the DAG:
   - Reads the raw dataset from `/app/raw_data.jsonl`.
   - Pipes it through your compiled Rust cleaner.
   - Uses the `sqlite3` CLI to bulk import the cleaned stdout stream into a SQLite database at `/home/user/clean_data.db` under a table named `readings`.

You will need to install any standard tools (like `ffmpeg`, Python transcription libraries like `openai-whisper`, or `sqlite3`) yourself. The agent environment is a standard Linux terminal.