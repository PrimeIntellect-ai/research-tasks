You are a localization engineer dealing with an ETL job that aggregates incoming translation updates from freelancers. Unfortunately, the job has a bug: it often retries on network failures, resulting in duplicate records. Additionally, some records contain corrupted text due to encoding issues.

Your task is to write a Rust command-line tool that processes these translation updates, filters out anomalies, deduplicates retries, and reshapes the data into a clean, wide-format JSON dictionary.

There is an initialized Rust project at `/home/user/loc_etl`. You must implement the logic in this project and compile it to a release binary.

**Input Format:**
The program must read from `stdin`. The input is a stream of JSON Lines (JSONL).
Each line is a JSON object with the following fields:
- `timestamp` (integer)
- `key` (string)
- `lang` (string)
- `text` (string)

**Processing Rules:**
1. **Anomaly Detection:** Drop any record where the `text` field contains the Unicode Replacement Character (`\u{FFFD}`).
2. **Deduplication:** For any given `key` and `lang` combination, retain only the record with the highest `timestamp`. If multiple records share the same highest timestamp, keep the one that appears *last* in the input stream.
3. **Reshaping:** Transform the flat records into a nested dictionary structure.
4. **Additional Rule:** There is a short audio memo from the lead engineer located at `/app/audio_instructions.wav`. You must listen to or transcribe this audio file and implement the additional filtering rule described in it.

**Output Format:**
The program must write the final result to `stdout`.
- The output must be a single, valid, minified JSON object.
- The structure must be: `{"<key>": {"<lang>": "<text>"}}`
- The top-level object must have its keys (the translation keys) sorted alphabetically.
- The nested objects (the languages) must also have their keys sorted alphabetically.
- Keys that end up with no valid translations (because all records were filtered out) should not be included in the output.

Build your final executable in release mode so it is located at `/home/user/loc_etl/target/release/loc_etl`. We will test your binary against an automated fuzzer comparing it to our reference implementation.