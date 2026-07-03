You are a data engineer tasked with building a lightweight ETL pipeline in Python to process a malformed JSON-Lines log file. The upstream system occasionally emits broken unicode escape sequences that cause standard JSON parsers to fail.

Write a Python script at `/home/user/etl_pipeline.py` that implements a pipeline to process this data. You must use the `jinja2` package for template generation (you may need to install it).

Your pipeline must execute the following logical steps in order:

1. **Extract and Clean:**
   Read the file at `/home/user/data/raw_events.jsonl`. This file contains one JSON object per line. Some lines contain invalid unicode escape sequences (e.g., `\uZZZZ`) which break `json.loads()`. 
   Before parsing each line, use a regular expression to find any `\u` followed by exactly 4 characters where at least one character is NOT a valid hexadecimal digit (0-9, a-f, A-F). Replace each of these invalid 6-character sequences with the literal string `?`. 
   After cleaning the line, parse it as JSON. Each JSON object has an `id` and a `message`.

2. **Hash-based Deduplication:**
   Extract the `message` field from each parsed object. Compute the SHA-256 hash of the UTF-8 encoded `message` string. Deduplicate the records based on this hash, keeping only the **first** occurrence of each unique `message`. 

3. **Validation Checkpoint (Quality Gate):**
   Implement a validation function that takes the deduplicated messages and ensures:
   - There are at least 5 unique records.
   - There are absolutely no duplicate messages remaining.
   If either condition fails, the script should raise a `ValueError`.

4. **Template-Based Generation:**
   Use the Jinja2 template located at `/home/user/data/template.md.j2` to generate a Markdown report. 
   Pass the deduplicated messages to the template as a list of strings under the variable name `messages`.
   Save the rendered output to `/home/user/output/report.md`.

Ensure your script runs successfully and produces the final `/home/user/output/report.md` file when executed.