You are a localization engineer tasked with reviewing a massive translation update from a vendor. You need to identify sections of the file where the vendor might be using machine translation bloat (where the Spanish translation is abnormally long compared to the English source) and send a sample to the QA server.

You have a large JSONL file located at `/home/user/data/translations.jsonl`. Each line is a JSON object with keys: `id`, `en`, and `es`.

Write a Python script to do the following:
1. Stream the file `/home/user/data/translations.jsonl` line by line (do not load the entire file into memory, as in a real scenario this file would be hundreds of gigabytes).
2. For each line, calculate the character length ratio: `len(es) / len(en)`.
3. Maintain a rolling average of this ratio for the last 10 processed lines. (If fewer than 10 lines have been processed, average the ratios of the lines processed so far).
4. Whenever the rolling average strictly exceeds `2.0`, flag the current translation record. 
5. Extract a stratified sample consisting of exactly the *first 5* flagged records.
6. Save these 5 records as a single valid JSON array of objects to `/home/user/flagged.json`.
7. Transfer this file to the local QA server by sending an HTTP POST request to `http://127.0.0.1:8080/upload` with the exact contents of `/home/user/flagged.json` as the request body.

Note: 
- The QA server is already running on port 8080.
- Use Python 3. You may use shell commands like `curl` to perform the upload if you prefer.