You are an MLOps engineer tasked with validating text generation experiment artifacts. 

In `/home/user/artifacts/`, there are several CSV files containing the results of different model experiments. Each file has three columns: `id`, `ground_truth`, and `prediction`.

Your task is to write and execute a Python script that evaluates these experiments by computing the average cosine similarity between the Bag-of-Words (BoW) embeddings of the `ground_truth` and `prediction` for each row.

To ensure standardization, follow these exact rules for the embedding and similarity computation:
1. **Tokenization**: Lowercase both strings. Split the strings into tokens using standard whitespace separation. Do not remove punctuation (treat punctuation attached to words as part of the token).
2. **Embedding**: For each row, construct a Bag-of-Words frequency vector for both the ground truth and the prediction. The vocabulary should be the union of unique tokens in that specific pair of strings. The vector values should be the frequency (count) of each token.
3. **Linear Algebra**: Compute the Cosine Similarity between the two vectors: `(A dot B) / (norm(A) * norm(B))`. If either vector is completely empty (norm of 0), the similarity is 0.0.
4. **Aggregation**: For each CSV file, compute the arithmetic mean of the cosine similarities for all rows.

Determine which experiment CSV has the highest average similarity score. Write your final answer to `/home/user/best_experiment.txt`. 

The file must contain exactly one line with the format:
`[filename.csv]: [score]`
Where `[score]` is rounded to exactly 4 decimal places (e.g., `0.1234`).