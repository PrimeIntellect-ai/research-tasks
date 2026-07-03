You are acting as a Machine Learning Engineer. A junior data scientist has written a machine learning script located at `/home/user/train_model.py` to classify text data. 

The script reads data from `/home/user/data.csv`, extracts TF-IDF embeddings, and uses a K-Nearest Neighbors classifier to perform similarity search and classification. It also uses `GridSearchCV` to find the best `n_neighbors`.

However, the script has a severe **data leakage flaw**: the `TfidfVectorizer` is fitted and transforms the entire dataset *before* the train/test split and before cross-validation. This violates best practices because information from the test set and validation folds leaks into the training process via the IDF weights and vocabulary.

Your task is to fix this script:
1. Refactor the code to use an `sklearn.pipeline.Pipeline`. Combine the `TfidfVectorizer` (named `'tfidf'`) and `KNeighborsClassifier` (named `'knn'`) into a single pipeline.
2. Ensure the train/test split happens *before* any transformations are applied to the text data. Use `test_size=0.2` and `random_state=42`.
3. Apply `GridSearchCV` on the **pipeline** itself to prevent leakage during cross-validation. Set `cv=5`.
4. The grid search must tune both:
   - `tfidf__max_features`: test the values `[50, 100]`
   - `knn__n_neighbors`: test the values `[3, 5, 7]`
5. After fitting the grid search on the training data, evaluate it on the test set.
6. Write the results to `/home/user/fixed_result.txt` in the following exact format:
```
Test Score: <score rounded to 4 decimal places>
Best Params: <the grid.best_params_ dictionary>
```

You must run your fixed script to generate the output file. You may use any standard shell tools or modify the Python script directly. Do not change the random state or CV split sizes.