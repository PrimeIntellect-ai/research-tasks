You are a data engineer tasked with building a reproducible ETL and modeling pipeline. We have a raw dataset of text messages that needs to be cleaned, processed, and used to train a simple Bayesian model.

Write a Python script at `/home/user/etl_pipeline.py` that performs the following steps:
1. **Data Loading**: Read the dataset from `/home/user/raw_data.csv`. The dataset has columns `id`, `text`, and `label`.
2. **Missing Value Handling**: Drop any rows where either `text` or `label` is missing (NaN/null).
3. **Dataset Preparation & Tokenization**: Use `sklearn.feature_extraction.text.CountVectorizer` with `lowercase=True` and `stop_words='english'` to transform the `text` column into a bag-of-words matrix.
4. **Reproducible Splitting**: Split the transformed data and the `label` column into training and testing sets using `sklearn.model_selection.train_test_split`. Use `test_size=0.3` and `random_state=42` to ensure the pipeline's reproducibility.
5. **Bayesian Modeling**: Train a `sklearn.naive_bayes.MultinomialNB` model on the training set using default parameters.
6. **Evaluation**: Predict the labels for the test set and calculate the accuracy score using `sklearn.metrics.accuracy_score`.
7. **Reporting**: Write the final test accuracy to `/home/user/metrics.json` in the exact format: `{"accuracy": <float_value>}`.

Ensure that your script is self-contained and runs without errors. Run the script so that the `metrics.json` file is produced.