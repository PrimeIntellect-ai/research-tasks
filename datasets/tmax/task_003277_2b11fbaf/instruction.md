You are a data scientist tasked with cleaning a messy dataset of document snippets. 

You have been provided with a CSV file at `/home/user/dataset.csv` containing three columns: `doc_id`, `title`, and `text`. 
Your goal is to identify near-duplicates using text embeddings, remove them, and apply dimensionality reduction for downstream visualization.

Please write a script (or a combination of shell commands and code) to perform the following steps exactly as described:

1. **Embedding Computation**: Compute TF-IDF vectors for the `text` column. Use scikit-learn's `TfidfVectorizer` with default parameters.
2. **Similarity Search**: Calculate the cosine similarity between all pairs of documents. Identify the 3 pairs of documents that have the highest cosine similarity (excluding self-similarity). 
3. **Log Duplicates**: Save these 3 pairs into a JSON file at `/home/user/duplicate_pairs.json`. The file should contain a single list of lists, where each inner list contains the two `doc_id` integers of a similar pair. Within each inner list, the smaller ID should come first. Order the outer list by similarity score in descending order (highest similarity first). 
4. **Data Cleaning**: Create a new dataset that drops exactly 3 documents. For each of the 3 pairs identified above, remove the document with the *larger* `doc_id`.
5. **Dimensionality Reduction**: Using the TF-IDF matrix of the *remaining* (cleaned) documents, apply `TruncatedSVD(n_components=2, random_state=42)` from scikit-learn. Add the resulting two dimensions as new columns named `pca_1` and `pca_2` to the cleaned dataset.
6. **Output**: Save the final cleaned dataset with the new PCA columns as a CSV file to `/home/user/cleaned_dataset.csv` (include headers, do not include pandas index).

Ensure your script runs successfully and generates both `/home/user/duplicate_pairs.json` and `/home/user/cleaned_dataset.csv`.