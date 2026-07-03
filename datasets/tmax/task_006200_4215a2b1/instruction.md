You are helping a researcher debug and fix an ETL and modeling pipeline. The researcher has written a Python script to tokenize text documents, compute TF-IDF features, and perform a similarity search to find the closest matches between a test set and a training set. 

However, there is a data leakage bug in the script: the `TfidfVectorizer` is being `fit_transform`ed on the entire dataset *before* the train/test split. This leaks vocabulary and inverse document frequency (IDF) statistics from the test set into the training phase, artificially inflating the numerical accuracy of the similarities.

Your task is to:
1. Inspect the buggy script located at `/home/user/process_data.py` and the dataset at `/home/user/data/articles.csv`.
2. Fix the data leakage bug. The script must first split the raw text into training and test sets using `train_test_split` with `test_size=0.2` and `random_state=42`.
3. Apply the `TfidfVectorizer(max_features=100)` correctly: it should be *fit* only on the training text, and then used to *transform* both the training and test texts.
4. For each document in the test set, compute its maximum cosine similarity to any document in the training set. 
5. Calculate the mean of these maximum similarities across all test documents.
6. Create the directory `/home/user/output/` if it doesn't exist.
7. Save the corrected mean maximum similarity, rounded to exactly 4 decimal places, into `/home/user/output/metrics.txt`.

Ensure your corrected script runs successfully and produces the expected output file.