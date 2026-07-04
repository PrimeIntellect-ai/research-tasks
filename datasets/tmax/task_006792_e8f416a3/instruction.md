You are a data scientist cleaning a web-scraped dataset. The file `/home/user/scraped_data.jsonl` contains scraped documents in JSON-lines format. Due to errors in the scraping process, some lines contain malformed JSON (specifically, invalid unicode escape sequences like `\u000g` or truncated structures). Furthermore, many scraped documents contain the exact same content in their `body` field.

Your task is to build a multi-stage data cleaning pipeline directly in the terminal to process this dataset. 

You must execute the following pipeline:
1. **Validation Checkpoint**: Read `/home/user/scraped_data.jsonl` and filter out any lines that are not valid JSON. 
2. **Quality Gate Metric**: Count the number of strictly valid JSON lines and write this single integer to `/home/user/valid_count.txt`.
3. **Hash-Based Deduplication**: For the valid JSON lines, calculate a hash (e.g., MD5) of the `body` field. Deduplicate the records so that only one JSON line per unique `body` remains. 
4. **Conflict Resolution**: When multiple valid JSON lines have the same `body`, you must keep the one that appeared **first** in the original file.
5. **Final Output**: Write the deduplicated valid JSON lines to `/home/user/clean_data.jsonl`. The order of the lines in the final file does not matter, as long as the exact correct JSON objects are preserved.

You may use standard shell tools (like `jq`, `awk`, `sort`, `md5sum`) or write a script in any language (e.g., Python, Node.js) to accomplish this. 

**Verification:**
An automated test will check:
- The existence and exact integer content of `/home/user/valid_count.txt`.
- The exact set of JSON objects in `/home/user/clean_data.jsonl` (independent of line order).