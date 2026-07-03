You are a data analyst working on processing a dataset of product descriptions. You have been given a CSV file located at `/home/user/data.csv`. 

Your goal is to build a highly reproducible feature engineering and embedding pipeline. 

Write a Python script at `/home/user/pipeline.py` that performs the following steps:
1. Reads `/home/user/data.csv`.
2. Creates a new feature called `text_length`, which is the character count of the `text` column.
3. Computes dense embeddings for the `text` column. To do this without downloading large neural networks, use `sklearn.feature_extraction.text.TfidfVectorizer` (with default parameters) followed by `sklearn.decomposition.TruncatedSVD` with `n_components=2` and `random_state=42`. Name the resulting dimensions `emb_0` and `emb_1`.
4. Saves the resulting dataset to `/home/user/output.csv` with the columns exactly in this order: `id`, `price`, `text_length`, `emb_0`, `emb_1`. Output the CSV without the index (`index=False`) and round all floating-point numbers to 4 decimal places.

Crucial Constraints for Reproducibility:
- Your script must explicitly set the environment variable `OPENBLAS_NUM_THREADS` to `"1"` inside the Python code *before* importing any numerical libraries.
- Set the global random seeds for `numpy` and standard `random` to `42` at the start of your script.
- Ensure that multiple runs of your script produce the exact same `/home/user/output.csv` file. 

Run your script to generate the `/home/user/output.csv` file.