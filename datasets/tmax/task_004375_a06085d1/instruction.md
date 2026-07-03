As an MLOps engineer, I need to track down a specific experiment artifact based on a screenshot of an old dashboard, and analyze its related metrics. 

I have an image at `/app/query.png` which contains a search query for an experiment log. 
I also have a dataset of experiment logs at `/app/logs.json`. The JSON is a list of dictionaries with keys: `id`, `log_text`, `latency_ms`, and `vram_mb`.

Please perform the following multi-language pipeline:
1. Write a shell script (or use CLI tools directly) to perform OCR on `/app/query.png` (Tesseract is installed) to extract the exact text of the query. The text will be prefixed with "Query: ". Ignore the prefix and keep only the query string itself.
2. Write a Python script to do the following:
   a. Tokenize the `log_text` of all entries in `/app/logs.json` (lowercase, remove punctuation, split by whitespace).
   b. Construct a TF-IDF representation of the logs corpus (you may use `scikit-learn`).
   c. Transform the extracted search query using the same TF-IDF vectorizer.
   d. Compute the cosine similarity between the query vector and all log vectors.
   e. Save the similarity results to `/app/similarities.csv` with the header `id,score`, sorted by `id` in ascending order.
   f. Filter the dataset to include only logs with a similarity score > 0.05. Calculate the covariance matrix between `latency_ms` and `vram_mb` for this subset. Save the trace of this covariance matrix (the sum of the diagonal elements) to `/app/cov_trace.txt` as a single floating-point number.

Your final output must include `/app/similarities.csv` and `/app/cov_trace.txt`.