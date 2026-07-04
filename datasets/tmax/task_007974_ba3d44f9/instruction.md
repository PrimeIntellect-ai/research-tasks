I am a researcher organizing text datasets for an NLP project. I have a Python pipeline that is supposed to join a metadata CSV file with a raw text JSONL file, tokenize the text, and output a prepared dataset. 

However, right now my script is running but producing a completely empty output file (similar to how a misconfigured matplotlib backend might produce a blank plot without throwing an error). The join operation is failing silently due to a mismatch in ID formats between the two sources.

Here is the setup:
- `/home/user/data/metadata.csv` contains `doc_id` (format: "DOC_#"), `category`, and `date`.
- `/home/user/data/texts.jsonl` contains `id` (format: integer #) and `content` (raw text strings).

Your task:
1. Fix the join condition. You must write a Python script at `/home/user/process.py` that loads both datasets and correctly joins them. The `id` in `texts.jsonl` (e.g., `1`) corresponds to the `doc_id` in `metadata.csv` (e.g., `DOC_1`).
2. Add a tokenization step to the script. For the `content` field in the joined data, extract a list of tokens. A token is defined strictly as a contiguous sequence of lowercase alphanumeric characters. Use the regex `\b[a-z0-9]+\b` on the lowercased text.
3. The script must output the final joined and tokenized data to `/home/user/output/processed.jsonl`. This file must be in JSON Lines format, where each line is a JSON object containing exactly three keys: `doc_id` (string), `category` (string), and `tokens` (list of strings).
4. Create a `Makefile` at `/home/user/Makefile` with a target `all` that runs your `process.py` script. 

Ensure the `output` directory exists or is created by your script. Only records that exist in *both* datasets should be included in the final output.