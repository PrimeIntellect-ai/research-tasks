You are helping a data scientist debug a Rust pipeline used for natural language dataset preparation. The pipeline tokenizes a small text corpus, finds the top 3 most frequent tokens, and calculates the covariance matrix of their occurrence across documents to understand word relationships before model training.

Currently, much like a matplotlib script configured with a headless backend that outputs blank plots, this Rust script completes successfully but outputs a matrix of all zeros (or fails to find any words) due to a parsing misconfiguration in the text preprocessing step. 

Your task:
1. Navigate to `/home/user/nlp_tools`.
2. Inspect the Rust project and its source code in `src/main.rs`. You will find that the text normalization and tokenization step is severely flawed, filtering out the actual content.
3. Fix the bug in `src/main.rs`. The tokenization should:
   - Convert all text to lowercase.
   - Remove all characters EXCEPT alphabetic characters (a-z) and spaces.
   - Split the resulting string into tokens by whitespace.
4. Ensure the script correctly calculates the top 3 most frequent tokens across the entire corpus (by total count).
5. Ensure the script calculates the 3x3 covariance matrix of these 3 tokens' frequencies per document. (The formula used in the boilerplate is Sample Covariance).
6. Build and run the project using `cargo`.
7. The script must output the top 3 tokens (one per line) to `/home/user/output/top_tokens.txt` (ordered by descending frequency).
8. The script must output the 3x3 covariance matrix to `/home/user/output/covariance.csv`, formatted with 4 decimal places of precision, comma-separated.

The input corpus is located at `/home/user/data/corpus.txt`.
You may edit `src/main.rs` as needed, but do not change the mathematical logic for the covariance calculation, only the text preprocessing/tokenization steps.