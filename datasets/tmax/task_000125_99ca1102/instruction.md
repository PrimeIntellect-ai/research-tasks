You are an ML Engineer preparing a mathematical dataset for a sequence-to-sequence model. 

Your task is to build a simple ETL and tokenization pipeline in Python that processes raw equations, filters out dirty data, and tracks experiment metrics.

1. First, create the necessary environment directories:
   - `/home/user/data/processed`
   - `/home/user/metrics`

2. You have a raw text file located at `/home/user/data/raw/equations.txt`. Write and execute a Python script (`/home/user/prepare_data.py`) using only standard libraries to process this file line-by-line according to the following rules:
   - Strip leading/trailing whitespace and convert the line to lowercase.
   - **Filter:** Discard any line that contains characters *other* than letters (`a-z`), digits (`0-9`), periods (`.`), spaces (` `), and the math symbols `+`, `-`, `*`, `/`, `=`, `(`, `)`.
   - **Tokenize:** For valid lines, split the string into a list of tokens. A token is defined as either:
     - A contiguous sequence of digits (which may contain a single period, e.g., `3.14` or `2`).
     - A contiguous sequence of letters (e.g., `x`, `y`, `func`).
     - A single math symbol (`+`, `-`, `*`, `/`, `=`, `(`, `)`).
     *(Hint: `2x` should become `['2', 'x']`. Ignore spaces during tokenization).*
   
3. **Outputs:**
   - Save the valid tokenized lines to `/home/user/data/processed/tokenized.jsonl`. Each line must be a valid JSON object in the exact format: `{"tokens": ["token1", "token2", ...]}`
   - Track your ETL metrics and save them to `/home/user/metrics/run_log.json`. The JSON file must contain exactly these keys:
     - `"total_lines"`: (integer) Total number of lines in the raw file.
     - `"valid_lines"`: (integer) Number of lines that passed the filter.
     - `"vocab_size"`: (integer) The total number of *unique* tokens across all valid lines.

Run your script so the output files are generated.