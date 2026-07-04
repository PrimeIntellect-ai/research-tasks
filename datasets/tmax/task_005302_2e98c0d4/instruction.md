You are an AI assistant acting as a data scientist. You have been tasked with cleaning a dataset of product features and generating recommendations.

You are provided with:
1. A dataset at `/app/dataset.csv` containing product embeddings (columns `id`, `f1` to `f20`). The dataset contains some missing values (`NaN`) and severe outliers due to sensor errors.
2. An image at `/app/settings.png` containing a handwritten note with the outlier threshold parameter you must use.

Your task is to:
1. Read the parameter from `/app/settings.png` using OCR (e.g., Tesseract). The image contains text in the format `outlier_z_threshold = X.X`.
2. For each feature column (`f1` to `f20`), calculate the standard z-score (ignoring NaNs). Identify outliers as any value with an absolute z-score strictly greater than the extracted threshold. Replace these outlier values with `NaN`.
3. Impute all missing values (both the original missing values and the ones you just created from outliers). You must use `IterativeImputer` from `sklearn.impute` with a `BayesianRidge` estimator. Leave the `BayesianRidge` parameters as default, but set `random_state=42` and `max_iter=20` in the `IterativeImputer`.
4. After the dataset is completely cleaned and imputed, perform a similarity search. For the products with `id` from `0` to `49`, find the top 3 most similar *other* products in the entire dataset based on cosine similarity.
5. Save these recommendations to `/home/user/top_similar.json`. The file must be a JSON dictionary where the keys are the string representation of the query product IDs (e.g., `"0"`, `"1"`, ..., `"49"`), and the values are lists of the top 3 similar product IDs as integers (e.g., `{"0": [45, 128, 9], "1": ...}`).

Ensure your similarity search properly excludes the query item itself from its own recommendations.