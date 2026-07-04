You are an assistant helping a data scientist clean a messy, multi-lingual dataset received from different regional offices. 

You have a directory of raw incoming text files at `/home/user/raw_data/`. Each file contains one text record per line, but the files were saved with different character encodings (UTF-8, ISO-8859-1, and UTF-16LE). Furthermore, some records are identical but appear in multiple files, sometimes with different Unicode normalizations.

Your task is to build an automated data cleaning pipeline.

Write a Python script at `/home/user/clean_pipeline.py` that does the following:
1. Finds all `.txt` files in `/home/user/raw_data/`.
2. Processes the files **in parallel** (using Python's `concurrent.futures` or `multiprocessing`).
3. Safely decodes each file. You must attempt to decode each file using UTF-8, ISO-8859-1, and UTF-16LE (fallback through them until successful).
4. For every line in every file, strip leading/trailing whitespace and normalize the text to Unicode **NFC** form.
5. Deduplicate the records across all files based on the SHA-256 hash of the normalized text. 
6. Output the unique records to a JSONL file at `/home/user/clean_data/deduped_output.jsonl`.
   - Each line in the JSONL file must be a JSON object with exactly two keys: `"hash"` (the hex digest of the SHA-256 hash of the UTF-8 encoded normalized text) and `"text"` (the normalized string itself).
   - If `/home/user/clean_data/` does not exist, your script should create it.

Finally, schedule this script to run daily at 2:00 AM using the user's crontab. The cron job should execute the script using `/usr/bin/python3`.

Please install any necessary standard packages, write the script, and configure the cron job. When you are done, run your script once manually to generate the output file so it can be verified.