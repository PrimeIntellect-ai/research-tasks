You are a Machine Learning Engineer working on preparing a text classification model. 

In your workspace (`/home/user/`), you have a script named `train_model.py` and a dataset `raw_data.csv`. The script currently processes the text using TF-IDF, reduces dimensionality using PCA, and trains a Logistic Regression model.

However, the current implementation contains a critical methodological flaw: **data leakage**. The original author applied the `TfidfVectorizer` and `PCA` transformations on the *entire* dataset before splitting it into training and testing sets. This leaks information from the test set into the training process, resulting in unreliable evaluation metrics.

Your task is to:
1. **Clean the dataset**: First, create a script or use command-line tools to process `raw_data.csv` into a new file `/home/user/clean_data.csv`. You must lowercase all the text in the "text" column and remove all punctuation (specifically `!` and `?`). Retain the CSV structure (header `text,label`).
2. **Fix the Data Leakage**: Edit `/home/user/train_model.py` to correctly split the data into training and testing sets *before* applying the TF-IDF and PCA transformations. 
   - You must fit the `TfidfVectorizer` and `PCA` ONLY on the training data, and then transform both the training and testing sets.
   - Keep the existing hyperparameters (`test_size=0.3`, `random_state=42` for all splits/models, `max_features=50`, `n_components=10`).
3. **Run the Pipeline**: Execute the fixed `train_model.py`. The script is already designed to compute the test set accuracy and output it to `/home/user/metrics.json`. Make sure this file is successfully generated with the new, corrected accuracy.

Make sure the final `metrics.json` file contains the exact JSON format: `{"accuracy": <float>}`.