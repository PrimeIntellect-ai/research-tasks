You are an AI assistant helping a data science researcher organize and preprocess a dataset of research text using Rust. 

The researcher has a raw dataset located at `/home/user/raw_data.jsonl`. 
You need to write and execute a Rust program that performs data schema enforcement, tokenization, and a simple dimensionality reduction (feature hashing) to prepare the data for model training.

Please perform the following steps:
1. Create a new Rust project (e.g., in `/home/user/preprocessor`). You can use popular crates like `serde` and `serde_json`.
2. Read the file `/home/user/raw_data.jsonl`.
3. **Schema Enforcement:** The expected schema for each JSON line is:
   - `doc_id`: unsigned 32-bit integer (`u32`)
   - `content`: string
   Any line that fails to match this schema perfectly (e.g., missing fields, wrong types) must be silently ignored and dropped from the pipeline.
4. **Tokenization:** For each valid document, extract the `content` string, convert the entire string to lowercase, and split it into tokens using standard whitespace as the delimiter.
5. **Dimensionality Reduction (Feature Hashing):** Convert the tokens into a fixed 4-dimensional feature vector `[f0, f1, f2, f3]` using the following deterministic hashing approach:
   - For each token, calculate the sum of the ASCII values of its characters.
   - The token's target dimension index is the ASCII sum modulo 4 (i.e., `sum % 4`).
   - Count the frequency of tokens mapping to each dimension to build the vector.
6. **Output:** Write the resulting feature vectors to a CSV file located exactly at `/home/user/features.csv`.
   - The CSV must have a header row: `doc_id,f0,f1,f2,f3`
   - Subsequent rows should contain the document ID and its 4-dimensional vector, sorted by `doc_id` in ascending order.
   - There should be no spaces after commas.

Ensure your code is compiled and run, and that `/home/user/features.csv` is generated successfully before you finish.