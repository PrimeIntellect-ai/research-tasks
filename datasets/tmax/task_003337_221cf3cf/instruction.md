You are an AI assistant helping a data science researcher organize a textual dataset and build a reproducible ETL and modeling pipeline. 

We have a two-service setup located in `/app/`:
1. A Redis database running locally.
2. A Flask API (`/app/api.py`) that serves our dataset from Redis. 

Currently, the Flask API is failing to connect to Redis because it is misconfigured. 

Your task is divided into the following stages:

**Stage 1: Multi-Service Pipeline Repair**
1. Inspect `/app/api.py` and fix the Redis connection parameters. The Redis service is running on the default port `6379`, but the API is configured to look elsewhere.
2. Restart the Flask API so it binds to port `5000`. Ensure it runs in the background.
3. Once fixed, you can access the training data at `http://127.0.0.1:5000/data/train` and the test data at `http://127.0.0.1:5000/data/test`. Both return JSON arrays of objects with the format: `{"id": int, "text": string, "label": int}` (for training, label is 0 or 1. For test, label is missing/null).

**Stage 2: ETL & Data Cleaning**
Write a script (in Python or Bash) to pull the training data and clean it:
1. **Missing Values**: Drop any records from the training data where the `label` is missing (`null`).
2. **Outliers**: Drop any records from the training data where the `text` field contains more than 50 words (words are separated by spaces).
3. **Tokenization**: Convert all text to lowercase. Split the text into tokens strictly by spaces. Keep only alphabetical characters and spaces (remove all punctuation before splitting).
4. Save the cleaned training data and the equally tokenized/cleaned test data (do not drop test items, just clean their text) into a structured format of your choice in `/home/user/`.

**Stage 3: Bayesian Inference Model in C**
Write a C program (`/home/user/naive_bayes.c`) that implements a Multinomial Naive Bayes classifier from scratch to calculate the posterior probability of class 1 for each test document.
1. The C program should read your cleaned training data to build a vocabulary and compute token frequencies for Class 0 and Class 1.
2. Apply Laplace (add-1) smoothing for all tokens present in the training vocabulary. Any tokens in the test set that never appeared in the training set should be completely ignored during probability computation.
3. Calculate the log-prior and log-likelihoods to avoid numerical underflow.
4. Convert the final log-probabilities back into a normalized probability for Class 1: `P(Class=1 | text)`.
5. The C program must output a CSV file at `/home/user/predictions.csv` with exactly two columns: `id,probability_class_1`. The first row must be the header.

Compile your C code and run it to produce `/home/user/predictions.csv`. Make sure your pipeline is reproducible and the final probabilities are as exact as possible.