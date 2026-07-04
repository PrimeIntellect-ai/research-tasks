You are a data analyst setting up an automated text processing pipeline to analyze customer feedback. The raw feedback is delivered as CSV files into a specific directory, but the text is messy—it contains raw unicode escape sequences (like `\u0021` instead of `!`) and inconsistent casing and punctuation.

Your task is to build a Python-based processing pipeline, wrap it in a shell script, and schedule it.

**Requirements:**

1. **Directories**:
   - Incoming files are dropped in `/home/user/incoming/` (already contains some initial CSV files).
   - Processed files should be moved to `/home/user/processed/`.
   - Your scripts should be placed in `/home/user/pipeline/`.
   - Create any directories that do not exist.

2. **The Python Script** (`/home/user/pipeline/process.py`):
   - Iterate through all `.csv` files in `/home/user/incoming/`.
   - Each CSV has two columns: `id` and `feedback`.
   - For each `feedback` entry, you must:
     - Decode any unicode escape sequences (e.g., `\u0021` becomes `!`, `\u002e` becomes `.`).
     - Convert all text to lowercase.
     - Remove all punctuation (equivalent to removing characters in Python's `string.punctuation`).
     - Tokenize the text into words by splitting on whitespace.
   - Aggregate the word counts across all processed files.
   - Load the existing word frequencies from `/home/user/pipeline/word_frequencies.json` (if it exists), add the new counts to it, and save the updated counts back to the same JSON file. The JSON file should be a flat dictionary mapping words (strings) to counts (integers).
   - Move the processed CSV files to `/home/user/processed/`.

3. **The Wrapper Script** (`/home/user/pipeline/run.sh`):
   - Create a bash script that executes the Python script.
   - Ensure it is executable.

4. **Scheduling**:
   - Set up a cron job for the current user (`user`) that executes `/home/user/pipeline/run.sh` every 10 minutes.

5. **Execution**:
   - Run your wrapper script manually once so that the initial files in `/home/user/incoming/` are processed and `/home/user/pipeline/word_frequencies.json` is generated for verification.