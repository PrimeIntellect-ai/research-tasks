You are a data scientist tasked with cleaning a messy dataset of system logs and building a baseline anomaly detection model. You must use a combination of shell commands (awk/bash) and Python to complete this pipeline.

The raw dataset is located at `/home/user/data/logs.csv` and has the following columns:
`id,response_time,message,is_anomaly`

Perform the following steps exactly as specified:

1. **Data Cleaning (Using Bash/Awk):**
   - Read `/home/user/data/logs.csv`.
   - Remove any rows where `response_time` is strictly less than 0 or strictly greater than 5000 (these are outliers).
   - For rows where `response_time` is missing (represented exactly as the string `NA`), impute the value by replacing `NA` with the integer `250`.
   - Save the cleaned dataset to `/home/user/data/cleaned_logs.csv`. Keep the header intact.

2. **Tokenization and Model Tuning (Using Python):**
   - Write a Python script to load `/home/user/data/cleaned_logs.csv`.
   - Tokenize the `message` column by converting all text to lowercase and splitting by whitespace. Use `sklearn.feature_extraction.text.TfidfVectorizer` with `max_features=50`, `stop_words='english'`, and default tokenization (just pass the raw text series to `fit_transform` after lowercasing).
   - Combine the 50 TF-IDF features with the `response_time` column to form your feature matrix (51 features total).
   - The target variable is `is_anomaly`.
   - Use `sklearn.linear_model.LogisticRegression(random_state=42, max_iter=1000)`.
   - Perform a Grid Search with 5-fold cross-validation (`sklearn.model_selection.GridSearchCV`, `cv=5`) to tune the inverse regularization parameter `C`. Test the following values for `C`: `[0.01, 0.1, 1.0, 10.0]`.
   - Note: Do not scale the `response_time` feature for this baseline.

3. **Reporting:**
   - Output the best parameter and its mean cross-validated score to `/home/user/metrics.txt` in exactly the following format:
     `Best C: <value>`
     `Best CV Score: <score_rounded_to_4_decimal_places>`
     Example:
     `Best C: 1.0`
     `Best CV Score: 0.8421`

Ensure your final output file `/home/user/metrics.txt` is perfectly formatted.