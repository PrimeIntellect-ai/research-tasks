You are a Data Scientist cleaning a dataset entirely via the command line. You need to write a Bash script that enforces data schema, reconstructs a simple scoring model for output validation, and removes duplicates. 

Write a bash script located at `/home/user/pipeline.sh` that processes a raw dataset at `/home/user/raw_data.jsonl` and outputs the cleaned data to `/home/user/cleaned_data.jsonl`.

The raw dataset contains JSON lines. Your Bash script must perform the following steps sequentially:

1. **Data Schema Enforcement:** 
   Filter the dataset to include only valid JSON lines that strictly contain the following fields with the correct types:
   - `id`: integer
   - `text`: string
   - `summary`: string
   If a row has missing fields, extra fields, or incorrect types, it must be discarded.

2. **Model Architecture Reconstruction & Inference:**
   You have been provided a linear model's weights in `/home/user/weights.tsv`. The file contains two tab-separated values: `w_text` and `w_summary`.
   The model computes a quality score based on the character lengths of the `text` and `summary` fields:
   `score = (w_text * length_of_text) + (w_summary * length_of_summary)`
   Your bash script must reconstruct this scoring logic. Calculate the score for each valid row. Only keep rows where `15.0 <= score <= 100.0`. 

3. **Deduplication (Embedding Retrieval approximation):**
   After scoring, keep only the *first* occurrence of each unique `text` (based on exact string matching). Discard any subsequent rows that have a `text` value identical to an already processed row.

Ensure your script `/home/user/pipeline.sh` is executable and writes the final surviving JSON lines to `/home/user/cleaned_data.jsonl` in the exact same format as the input.