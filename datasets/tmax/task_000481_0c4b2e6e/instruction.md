You are an analyst tasked with building an end-to-end data processing pipeline for customer reviews. You have a raw dataset located at `/home/user/raw_reviews.csv` with the following columns: `ID,Date,Status,Review_Text`. 

Your goal is to perform ETL, tokenization, embedding generation, dimensionality reduction, and clustering to find the most representative review of a specific customer segment.

Please complete the following steps:
1. **ETL Pipeline**: The raw CSV contains malformed rows, empty lines, and unverified reviews. Using standard bash command-line tools (e.g., `awk`, `grep`, `sed`), extract only the rows where the `Status` column is exactly `Verified`. Make sure the CSV header is retained. Save the output to `/home/user/clean_reviews.csv`.

2. **Feature Engineering & Dimensionality Reduction**: Write a Python script (`/home/user/pipeline.py`) that reads `clean_reviews.csv`. 
   - Tokenize the `Review_Text` by using `sklearn.feature_extraction.text.TfidfVectorizer`. Configure it to use `stop_words='english'` and `max_features=200`.
   - Reduce the resulting TF-IDF sparse matrix to 5 dimensions using `sklearn.decomposition.TruncatedSVD`. Set `n_components=5` and `random_state=42`.

3. **Model Training**: 
   - On the 5-dimensional dataset, train a K-Means clustering model using `sklearn.cluster.KMeans`. 
   - Set `n_clusters=4`, `n_init=10`, and `random_state=42`.

4. **Embedding Retrieval**:
   - Identify all data points assigned to Cluster `0`.
   - Calculate the Euclidean distance from each point in Cluster 0 to the centroid of Cluster 0.
   - Find the `ID` of the review that is closest to the centroid of Cluster 0.
   - Write ONLY that single integer `ID` to `/home/user/representative_review.txt`.

Ensure your Python script relies on `scikit-learn` and `pandas` (which are already installed). Execute your pipeline so the final text file is produced.