You are tasked with building a Go-based ETL data sanitization pipeline for a configuration management system. Our configuration agents recently had a bug in their retry logic, causing them to emit duplicate configuration state logs when network timeouts occurred. 

You need to write a Go CLI tool that processes JSON Lines (JSONL) log files, cleans them, and removes these erroneous duplicate records. 

An architecture diagram and specification notes have been left on a whiteboard, a photo of which is available at `/app/config_spec.png`. You must read this image (using OCR like `tesseract` or manual inspection) to extract two critical parameters for your logic: the `WINDOW_SIZE` (in seconds) and the `NORMALIZATION_PREFIX`.

**Pipeline Requirements:**

1. **Input/Output**: Your tool must be an executable Go program located at `/home/user/sanitizer.go`. It should take two arguments: the input file path and the output file path.
   `go run /home/user/sanitizer.go <input.jsonl> <output.jsonl>`

2. **Log Format**: Each line in the input is a JSON object with the following fields:
   - `id` (string)
   - `host` (string)
   - `ts` (integer, Unix timestamp)
   - `config_payload` (string)

3. **Normalization (Tokenization & Feature Extraction)**:
   Before processing a `config_payload`, you must normalize it:
   - Convert the payload to entirely lowercase.
   - Strip all whitespace characters (spaces, tabs, newlines).
   - Prepend the `NORMALIZATION_PREFIX` (extracted from the image) to the string.

4. **Imputation**:
   Some records have missing or zero timestamps (`ts`: 0). You must impute these missing timestamps. A missing timestamp should be linearly interpolated as exactly halfway between the `ts` of the *last valid record* for that specific `host` and the `ts` of the *next valid record* for that specific `host`. (You can assume the first and last records for any host in the file will always have valid timestamps, and there are never two missing timestamps in a row for the same host).

5. **Windowed Deduplication**:
   To fix the retry bug, you must apply a rolling window aggregation. If a record has the exact same *normalized* `config_payload` as a previously *accepted* record for the same `host`, AND its timestamp falls strictly within `WINDOW_SIZE` seconds of that previous record's timestamp (`ts - previous_ts <= WINDOW_SIZE`), it is considered a retry duplicate and MUST be dropped (omitted from the output). 

The output file must contain the sanitized JSONL records (with imputed timestamps updated, and duplicates dropped) preserving the original JSON keys. Valid records should otherwise remain exactly as they were (do not output the normalized payload, output the original `config_payload`).

We will evaluate your program against an adversarial corpus of logs. It must preserve 100% of the legitimate logs and successfully reject all duplicates in the corrupted logs.