You are a data engineer building a lightweight ETL and modeling pipeline for a text classification task.

We have a raw dataset located at `/home/user/data/raw_texts.csv` containing text snippets and their corresponding categories. The file has three columns: `id`, `text`, and `category`.

Your task is to write and execute a Python script that performs the following steps:
1. Load the data using `pandas`.
2. Split the dataset into training and testing sets using an 80/20 split. Use `sklearn.model_selection.train_test_split` with `random_state=42` and stratify based on the `category` column.
3. Build a single `scikit-learn` Pipeline with the following steps in order:
   - **Embedding:** `TfidfVectorizer` with `max_features=500`.
   - **Dimensionality Reduction:** `TruncatedSVD` with `n_components=50` and `random_state=42`.
   - **Model Training:** `LogisticRegression` with `random_state=42`.
4. Train this pipeline on the training set (predicting the `category` from the `text`).
5. Evaluate the pipeline on the test set and calculate the accuracy score.
6. Save the trained pipeline object to `/home/user/output/pipeline.pkl` using `joblib`.
7. Save the evaluation metrics to `/home/user/output/metrics.json` in the following exact format:
   `{"accuracy": <float_value>}`

Please ensure your script creates the `/home/user/output/` directory if it does not already exist. Run your script to generate the required output files.