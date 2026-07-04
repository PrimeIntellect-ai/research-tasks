You are a Machine Learning Engineer responsible for preparing a dataset for a new NLP model. Your objective is to build a reproducible data preparation pipeline in Python that joins multiple sources, enforces a strict schema, tokenizes text, and computes a feature using linear algebra.

You have been provided with two raw data files:
1. `/home/user/data/docs.csv`: Contains `doc_id` and `text`.
2. `/home/user/data/meta.csv`: Contains `doc_id`, `category`, and `date`.

Write a Python script `/home/user/prepare_pipeline.py` and run it to produce a final processed dataset at `/home/user/output/processed_data.jsonl`.

Your pipeline must perform the following steps:

1. **Multi-source joining**: Join the two CSV files on `doc_id` (inner join).
2. **Data schema enforcement**: 
   - Ensure `doc_id` can be parsed as an integer. Drop any rows where `doc_id` is missing or cannot be cast to an integer.
   - Ensure `category` is exactly one of the following: `['news', 'blog', 'wiki']`. Drop any rows that do not match.
3. **Tokenization**: 
   - Lowercase the `text` field.
   - Remove all characters except alphanumeric characters and spaces (e.g., remove punctuation).
   - Split the text by single spaces into a list of tokens. Drop empty strings from the list.
4. **Linear Algebra Feature Extraction**:
   - Identify the top 10 most frequent tokens across the entire *valid* (post-schema enforcement) dataset. Break ties by alphabetical order.
   - For each document, create a term-frequency (TF) vector of length 10 representing the counts of these top 10 tokens in the document.
   - Compute the L2 norm (Euclidean norm) of this vector for each document. Round the result to 4 decimal places. Name this feature `tf_l2_norm`.
5. **Output**:
   - Save the processed data to `/home/user/output/processed_data.jsonl`.
   - Each line should be a valid JSON object with the following keys exactly: `doc_id` (integer), `category` (string), `tokens` (list of strings), and `tf_l2_norm` (float).
   - The JSONL file must be sorted by `doc_id` in ascending order.

Create the output directory `/home/user/output` if it does not exist, and execute your pipeline so the final file is generated.