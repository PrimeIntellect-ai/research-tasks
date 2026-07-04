You are a data scientist tasked with cleaning a messy dataset of product reviews. The dataset is located at `/home/user/reviews.csv` and contains three columns: `id`, `text`, and `rating`. 

Unfortunately, the `rating` column has been corrupted. While most ratings are standard integers from 1 to 5, some values are completely out of bounds (e.g., -10, 50), and others are missing entirely (NaN). 

Your objective is to clean this dataset, run statistical tests on the corrupted vs. valid rows, and use a machine learning model to impute the missing and corrupted ratings based on the text content.

Please perform the following steps exactly as specified to ensure pipeline reproducibility:

1. **Data Preparation & Text "Embeddings"**:
   - Load `/home/user/reviews.csv`.
   - Drop any rows where the `text` column is missing (NaN).
   - Use `scikit-learn`'s `TfidfVectorizer` to convert the `text` column into feature vectors (which we will use as our embeddings). Set `max_features=500`, `stop_words='english'`, and `lowercase=True`.

2. **Hypothesis Testing**:
   - Split the dataset into two sets based on the original `rating`:
     - `valid_data`: Rows where the rating is between 1 and 5 (inclusive).
     - `corrupted_data`: Rows where the rating is strictly less than 1, strictly greater than 5, or missing (NaN).
   - We suspect that corrupted ratings might be associated with significantly shorter or longer review texts. Compute the length of the `text` (number of characters) for both groups.
   - Perform a Two-Sample independent T-test (using `scipy.stats.ttest_ind` with `equal_var=False`) to compare the mean text length of `valid_data` vs `corrupted_data`. Record the p-value.

3. **Model Training and Imputation**:
   - Train a `Ridge` regression model from `scikit-learn` (`alpha=1.0`, `random_state=42`) using the TF-IDF vectors of the `valid_data` as `X` and their `rating` as `y`.
   - Calculate the Mean Squared Error (MSE) of this model on its own training data (`valid_data`).
   - Use the trained model to predict the ratings for the `corrupted_data`.
   - **Validation & Clipping**: Ensure no predicted rating is outside the 1 to 5 range by clipping the predictions (values < 1 become 1.0, values > 5 become 5.0). 
   - Calculate the mean of these newly imputed (and clipped) ratings for the `corrupted_data`.

4. **Reporting**:
   - Save the fully cleaned dataset to `/home/user/cleaned_reviews.csv`. It must contain the columns `id`, `text`, and `final_rating`. The `final_rating` should be the original rating for `valid_data`, and the clipped predicted rating for `corrupted_data`. Ensure the rows are sorted by `id` in ascending order.
   - Save a JSON file to `/home/user/metrics.json` containing exactly these keys:
     - `"t_test_p_value"`: The p-value from your T-test (float).
     - `"train_mse"`: The MSE of the Ridge model on the valid data (float).
     - `"imputed_mean"`: The mean of the clipped imputed ratings for the corrupted data (float).

Note: You may need to install necessary Python libraries (like `pandas`, `scikit-learn`, `scipy`) using `pip`.