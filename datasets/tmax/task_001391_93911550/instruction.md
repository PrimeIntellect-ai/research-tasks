You are an AI assistant helping a data science researcher organize a dataset of research paper abstracts. 

The researcher has started building a Rust-based tool to compute document similarity and recommend related papers based on their abstracts. The project is located at `/home/user/paper_recommender`. 

However, there is a bug: the program runs and generates the output file, but all similarity scores seem to be resulting in empty or zeroed outputs, similar to a plotting script producing blank charts due to a misconfiguration. The researcher suspects there is a logical error in how the term frequencies or vectors are calculated in the Rust code.

Your task is to:
1. Examine the Rust project in `/home/user/paper_recommender`.
2. Identify and fix the bug(s) in `src/main.rs` that are causing the similarity calculations to fail (look closely at the mathematical operations and data types).
3. Build and run the project using the dataset provided at `/home/user/papers.json`.
4. Ensure the program outputs a CSV file at `/home/user/recommendations.csv`.

The output CSV must have the following format (no header):
`document_id,most_similar_id,second_most_similar_id`

Constraints:
- Do not use external crates for the math/TF-IDF logic; fix the existing manual implementation.
- Standard tokenization (lowercasing and splitting by whitespace) is already implemented and should be kept as is.
- Ignore a document's similarity to itself. 
- You must write your fix using Rust and use standard cargo commands to build and run.