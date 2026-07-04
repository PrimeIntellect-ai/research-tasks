You are a Machine Learning Engineer tasked with recovering corrupted training data and evaluating a model. A previous pandas pipeline silently converted some integer labels to floats by introducing `NaN` values. You need to impute these missing labels using text embeddings, find correlated features, and evaluate a baseline model.

Your tasks:
1. Set up your Python environment with `pandas`, `scikit-learn`, and `numpy`.
2. Load the dataset at `/home/user/data/dataset.csv`. It contains two columns: `text` and `target`.
3. Compute text embeddings for the `text` column using `sklearn.feature_extraction.text.TfidfVectorizer` with `max_features=50` and `stop_words='english'`.
4. **Impute missing targets (Retrieval)**: For every row where `target` is `NaN`, find its nearest neighbor among the rows with valid targets using cosine similarity of their TF-IDF vectors. Assign the `target` value of the nearest neighbor to the missing row. If there is a tie for highest similarity, pick the neighbor with the lowest original row index.
5. **Correlation Analysis**: Using *only the rows that originally had valid targets*, calculate the Pearson correlation coefficient between each of the TF-IDF features and the valid `target` values. Identify the index (0 to 49) of the TF-IDF feature with the highest positive correlation. Write this single integer to `/home/user/most_correlated_feature.txt`.
6. **Model Training**: Train a `sklearn.linear_model.LogisticRegression` (with `random_state=42` and all other parameters default) on the *entire* imputed dataset (X = TF-IDF features, y = imputed target).
7. **Bootstrap Evaluation**: Instead of a standard test set, evaluate the model using bootstrap sampling. Generate 1000 bootstrap samples of the imputed dataset. 
   - Initialize the random generator with `np.random.seed(42)` once before the loop.
   - For each of the 1000 iterations, sample row indices using `np.random.choice(len(df), size=len(df), replace=True)`.
   - Calculate the accuracy of the *already trained* Logistic Regression model on this sample.
   - Compute the 2.5th and 97.5th percentiles of these 1000 accuracy scores using `np.percentile`.
8. Write the lower and upper percentiles, separated by a comma and rounded to 3 decimal places, to `/home/user/bootstrap_ci.txt` (e.g., `0.751,0.892`).