You are a Machine Learning Engineer preparing training data for a new text classification model. You have a raw dataset, but it contains malformed entries and lacks the required text embeddings.

Write a Bash script at `/home/user/prepare_data.sh` that does the following:

1. Reads a raw JSONL dataset located at `/home/user/raw_data.jsonl`.
2. Enforces a strict data schema. A record is only valid if:
   - `id` exists and is a number.
   - `text` exists and is a string.
   - `label` exists and is exactly either the string `"POSITIVE"` or `"NEGATIVE"`.
3. Discards all invalid records.
4. From the valid records, sorts them in ascending order by their `id` and selects the first 5 records (deterministic sampling).
5. Computes a text embedding for each of the 5 selected records using the provided local embedding tool `/opt/embedder.py`. You can call this tool by passing the text as a command-line argument: `python3 /opt/embedder.py "your text here"`. It will output a JSON array representing the embedding (e.g., `[5, 2, 3]`).
6. Constructs a final JSONL output where each valid, sampled record retains its original `id`, `text`, and `label`, and includes a new field `embedding` containing the parsed JSON array from the embedder.
7. Saves the resulting 5 JSONL records to `/home/user/training_data.jsonl`.

Your script must be executable (`chmod +x /home/user/prepare_data.sh`) and use Bash to orchestrate the validation (`jq` is recommended), extraction, and processing. Run your script to generate `/home/user/training_data.jsonl` so it can be verified.