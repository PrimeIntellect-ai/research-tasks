You are a localization engineer managing the data processing pipeline for a new application. Your workflow involves receiving translated CSV files, validating them, processing them, and loading them into a local Translation Memory (TM) service.

There are three main parts to your task:

**Part 1: Service Composition**
You have three cooperating services in `/home/user/services/`:
1. `redis-server` (Standard Redis cache).
2. `tm_api.py` (A Flask API for the Translation Memory).
3. `tm_worker.sh` (A background bash process that ingests queued translations).

You must configure and start these services. 
- Redis should run on port `6379`.
- The Flask API (`tm_api.py`) defaults to port `5000`. It expects the environment variable `REDIS_URL` to point to the Redis instance (e.g., `redis://localhost:6379/0`).
- The worker (`tm_worker.sh`) expects a config file at `/home/user/services/worker.conf` containing `REDIS_PORT=6379` and `API_ENDPOINT=http://localhost:5000`. Create this file and start all three services in the background.

**Part 2: Adversarial Filtering**
Freelance translators sometimes provide files with corrupted formats or malicious XSS payloads. You must write a Bash script at `/home/user/filter.sh` that takes a CSV file path as its first argument and outputs ONLY the safe, valid lines to standard output. 
- The CSV format is `key,locale,translation`.
- A valid translation string may contain alphanumeric characters, spaces, punctuation, and balanced variable placeholders like `{username}`.
- A translation string MUST BE REJECTED (filtered out) if it contains any HTML/XML tags (e.g., `<script>`, `<b>`, `<img>`), unclosed/unbalanced curly braces `{` or `}`, or the word `javascript:`.
- Your filter will be tested against an internal "clean" corpus and an "evil" corpus. It must preserve 100% of the clean corpus and reject 100% of the malicious lines in the evil corpus.

**Part 3: The Processing Pipeline**
Write a Bash script at `/home/user/pipeline.sh` that takes a sanitized CSV file (output from Part 2) and performs the following ETL operations:
1. **Tokenization and Normalization:** Normalize the `locale` column (the second column) to the format `xx-YY` (lowercase two-letter language code, hyphen, uppercase two-letter country code). For example, `es_es`, `ES-ES`, or `es-es` should all become `es-ES`.
2. **Hash-based Deduplication:** If multiple lines have the exact same translation text (column 3) for the *same* normalized locale, keep only the first occurrence. Use a hash (like MD5) of the translation text + locale to track duplicates.
3. **Resampling and Gap-Filling:** Read a master list of keys from `/home/user/data/master_keys.txt`. For the target locale `es-ES`, if any key from the master list is missing in the data, fill the gap by appending a new row using the `en-US` translation from the file as a fallback. (Assume `en-US` translations for all keys exist in the input).
4. Save the final processed output to `/home/user/processed_translations.csv`.

Complete all scripts and ensure the services are running and correctly configured to talk to each other.