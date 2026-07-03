You are a data scientist working on cleaning and merging datasets from two separate systems that track item embeddings. Because the systems don't share exact foreign keys, you need to join them based on the mathematical similarity of their feature vectors.

You have two datasets located at:
- `/home/user/system_alpha.csv` (Columns: `item_id_alpha`, `f1`, `f2`, `f3`)
- `/home/user/system_beta.csv` (Columns: `item_id_beta`, `f1`, `f2`, `f3`)

Your task:
1. Write a Python script to compute the pairwise Cosine Similarity between all item vectors in `system_alpha` and all item vectors in `system_beta` using linear algebra operations (e.g., using `numpy`).
2. For each `item_id_alpha`, find the single `item_id_beta` that has the highest cosine similarity. (Assume there are no exact ties in this dataset).
3. Output the joined results to a new CSV file at `/home/user/matched_items.csv`.

The output file `/home/user/matched_items.csv` must:
- Have exactly the following headers: `item_id_alpha,item_id_beta,similarity`
- Have one row for every item in `system_alpha`.
- The `similarity` column must be rounded to exactly 4 decimal places (e.g., `0.9876`).

Please write and execute the Python code necessary to perform this mathematical join and create the final output file.