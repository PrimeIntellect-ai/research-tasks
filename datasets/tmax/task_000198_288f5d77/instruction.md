You are an algorithmic data scientist cleaning and preparing a merged dataset for modeling.

You have two disconnected datasets located in `/home/user/data/`:
1. `text.csv`: Contains columns `t_id`, `text_query`, and `doc_content`.
2. `stats.csv`: Contains columns `s_id`, `fuzzy_query`, `val_A`, `val_B`, and `target`.

Your task is to perform an end-to-end pipeline combining embedding retrieval, feature engineering, and cross-validation:

**Step 1: Data Merging via Embeddings**
The queries in `stats.csv` (`fuzzy_query`) are misspelled or slightly altered versions of the queries in `text.csv` (`text_query`).
* Compute TF-IDF embeddings for both query columns using `sklearn.feature_extraction.text.TfidfVectorizer` (use `analyzer='char'` and `ngram_range=(2,3)`).
* For each row in `stats.csv`, find the single best matching row in `text.csv` using Cosine Similarity between their query embeddings.
* Only keep matches where the Cosine Similarity is **strictly greater than 0.4**. Drop rows from `stats.csv` that do not have a match meeting this threshold.
* Join the matched data into a single DataFrame.

**Step 2: Feature Engineering**
* Create a new feature called `feature_X` which is the product of `val_A` and `val_B` (`val_A * val_B`).

**Step 3: Modeling & Cross-Validation**
You want to predict the `target` column using a Ridge Regression model. 
* Your feature matrix should consist of `feature_X` (scaled using `StandardScaler`) concatenated with TF-IDF embeddings of the `doc_content` column (use word-level TF-IDF, `ngram_range=(1,1)`, `max_features=100`, default stop words are not needed).
* Use `sklearn.model_selection.GridSearchCV` to tune a `Ridge` regression model.
* Search over the `alpha` parameter with values: `[0.1, 1.0, 10.0]`.
* Use 3-fold cross-validation (`cv=3`) without shuffling.
* Use Negative Mean Squared Error (`neg_mean_squared_error`) as the scoring metric.

**Output Generation**
Once you have found the best model, write the results to `/home/user/model_results.json`. The JSON file must strictly follow this structure:
```json
{
  "best_alpha": <float>,
  "mse": <float>
}
```
*Note: `mse` must be the absolute (positive) value of the best negative mean squared error score obtained during cross-validation, rounded to exactly 4 decimal places.*