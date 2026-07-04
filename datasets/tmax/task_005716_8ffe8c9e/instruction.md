You are a data engineer debugging an ETL pipeline for a recommendation system. 

We have a script located at `/home/user/etl_pipeline.py` that processes product descriptions to generate TF-IDF embeddings, performs a similarity search against a set of query items, and tracks the experiment results by logging the average top-1 cosine similarity score to a JSON file.

However, the pipeline has a critical "data leakage" bug in how the `TfidfVectorizer` is applied, causing the query vocabulary to leak into the training phase. This artificially inflates the similarity scores.

Your task:
1. Identify and fix the data leakage bug in the TF-IDF vectorization step. The vectorizer must ONLY be fitted on the training data, but it should be used to transform both the training data and the query data.
2. Save your corrected script as `/home/user/fixed_pipeline.py`. Modify the script so that it outputs its tracked metrics to `/home/user/experiment_v2.json` instead of `experiment_v1.json`.
3. Run both `/home/user/etl_pipeline.py` (which generates `/home/user/experiment_v1.json`) and your `/home/user/fixed_pipeline.py` (which generates `/home/user/experiment_v2.json`).
4. Validate the model output by calculating the absolute difference in the `avg_top1_similarity` between the two experiments. Write this absolute difference (a single float value) to `/home/user/leakage_diff.txt`.

Ensure your fixed Python script runs successfully and that all specified output files exist with the correct data formats.