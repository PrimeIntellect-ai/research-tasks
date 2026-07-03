I am a researcher organizing a text dataset into train and test splits, and trying to identify if any test documents are duplicates of training documents. 

Currently, I have a dataset at `/home/user/dataset.jsonl` with lines like `{"id": int, "text": str, "split": "train" | "test"}`.

I previously tried to find duplicates using a `sklearn.feature_extraction.text.TfidfVectorizer` to compute embeddings, but I made a classic mistake: I fitted the vectorizer on the *entire* dataset (train + test), which caused data leakage. 

I need you to write a Python script at `/home/user/organize.py` that fixes this and finds probabilistic duplicates. Your script must do the following:

1. **Embedding Computation**: Read the dataset. Fit a `TfidfVectorizer` (with default parameters) **only** on the `train` split. Then, transform both the `train` and `test` splits using this fitted vectorizer to get their embeddings.
2. **Retrieval**: Compute the pairwise cosine similarity between all `test` embeddings and all `train` embeddings. 
3. **Bayesian Output Validation**: Instead of just using a raw similarity threshold, I want to compute the posterior probability that a test document is a duplicate of a train document given their cosine similarity $S$. 
   Use Bayes' theorem: $P(\text{Dup} \mid S) = \frac{P(S \mid \text{Dup}) P(\text{Dup})}{P(S \mid \text{Dup}) P(\text{Dup}) + P(S \mid \text{Not Dup}) P(\text{Not Dup})}$
   Assume the following fixed parameters for my dataset:
   - Prior probability of any pair being a duplicate: $P(\text{Dup}) = 0.05$
   - Consequently, $P(\text{Not Dup}) = 0.95$
   - If $S \ge 0.7$, then $P(S \ge 0.7 \mid \text{Dup}) = 0.85$ and $P(S \ge 0.7 \mid \text{Not Dup}) = 0.02$
   - If $S < 0.7$, then $P(S < 0.7 \mid \text{Dup}) = 0.15$ and $P(S < 0.7 \mid \text{Not Dup}) = 0.98$
4. **Validation and Output**: Filter the test-train pairs. Only keep pairs where the posterior probability $P(\text{Dup} \mid S) > 0.5$. 
5. Save these valid duplicate pairs to `/home/user/duplicates.json` as a JSON array of objects, sorted descending by `prob`, then by `test_id` ascending, then by `train_id` ascending. Format of each object: `{"test_id": int, "train_id": int, "prob": float}` (round `prob` to 4 decimal places).

Please write and execute the script to produce the final `duplicates.json`.