You are tasked with fixing and completing a configuration log processing pipeline. 

A configuration manager outputs logs in JSON-lines format to `/home/user/raw.jsonl`. However, the system generating these logs encodes some ASCII characters as Unicode escape sequences (e.g., `\u0021` for `!`, `\u003D` for `=`), and it sometimes leaks sensitive values like passwords and API keys.

You need to build a pipeline to clean, anonymize, normalize, and deduplicate these logs.

**Step 1: The C Filter (`/home/user/filter.c`)**
Create a C program at `/home/user/filter.c` that reads standard input line-by-line (maximum 1024 characters per line) and writes to standard output. The program must perform the following operations on each line:
1. **Unicode Decoding:** Find any occurrences of `\u00XX` (where `X` is a valid uppercase or lowercase hex digit) and replace the 6-character sequence with the single corresponding decoded ASCII character. Assume all such sequences map to valid printable ASCII characters.
2. **Data Masking (Anonymization):** After decoding, check if the JSON line contains exactly `"key":"password"` or `"key":"api_key"`. If it does, you must mask its value. The value is always the last field in the JSON object and is formatted as `"val":"<actual_value>"}`. Replace `<actual_value>` with `***` so the end of the line becomes `"val":"***"}`. (Assume `<actual_value>` does not contain the substring `"` inside it).

**Step 2: The Orchestration Script (`/home/user/pipeline.sh`)**
Write a bash script at `/home/user/pipeline.sh` that performs the following pipeline orchestration:
1. Compiles `/home/user/filter.c` using `gcc` into an executable named `/home/user/filter`.
2. Reads the file `/home/user/raw.jsonl`.
3. Pipes the data through the compiled `filter` executable.
4. Sorts the output alphabetically.
5. Deduplicates the sorted output (removes identical lines).
6. Writes the final cleaned output to `/home/user/clean.jsonl`.

**Requirements:**
- Do not use external libraries in C (only standard library headers like `<stdio.h>`, `<stdlib.h>`, `<string.h>`).
- The bash script must use standard coreutils (e.g., `sort`, `uniq`).
- Ensure the bash script has executable permissions (`chmod +x`).
- Running `/home/user/pipeline.sh` should result in the correctly formatted `/home/user/clean.jsonl` file.