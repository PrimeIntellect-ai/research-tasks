You are tasked with cleaning a dataset of system logs and extracting features using a legacy tool. 

You have a dataset at `/home/user/data/events.jsonl`. Each line is a JSON object representing a system event, containing a `timestamp` (ISO 8601 format, e.g., `2023-10-12T14:30:00Z`), a `message` string, and other metadata.
We also have a proprietary, stripped binary located at `/app/legacy_extractor`. This tool reads JSON-lines from standard input and outputs a CSV with extracted features to standard output (format: `timestamp,feature_score`). 

However, `/app/legacy_extractor` has a known bug: if the `message` field contains unicode escape sequences (e.g., `\uXXXX`), the binary will crash with a segmentation fault, halting the pipeline. 

Your objective is to write a C program at `/home/user/cleaner.c` (and compile it to `/home/user/cleaner`) that performs the following:
1. Reads `/home/user/data/events.jsonl` line by line.
2. Sanitizes the JSON by replacing any backslash followed by a 'u' (`\u`) with `__` (two underscores) to prevent the legacy extractor from crashing.
3. Feeds the sanitized lines into `/app/legacy_extractor` via standard input.
4. Reads the CSV output from the extractor.
5. Parses the ISO 8601 `timestamp` from the extractor's output and converts it to a standard Unix epoch integer.
6. Writes the aligned results to `/home/user/output.csv` in the format: `unix_timestamp,feature_score`.
7. Generates a summary report at `/home/user/summary.txt` containing exactly: `Report: Processed <N> valid events.` (where `<N>` is the number of lines successfully processed and written).

Your solution will be evaluated based on the proportion of successfully extracted and correctly timestamp-aligned rows compared to a reference dataset. An automated metric will compute the row accuracy.

Requirements:
- Do not modify the original dataset.
- Your C program must orchestrate the data flow and transformation.
- The output file `/home/user/output.csv` must not contain a header.