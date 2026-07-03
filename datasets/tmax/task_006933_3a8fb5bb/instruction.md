You are a data analyst tasked with building a reproducible machine learning pipeline. You have a directory of chunked CSV files representing a large dataset, and you need to build a pipeline that processes this data, tunes a model, and stores the results securely in an HDF5 file. 

Here are your instructions:

1. **Environment Setup**: Ensure `pandas`, `scikit-learn`, and `h5py` are installed.
2. **Data Ingestion**: There are 5 CSV files located in `/home/user/data_chunks/` named `chunk_0.csv` to `chunk_4.csv`. Write a Python script at `/home/user/pipeline.py` that reads these files, sorts them by filename, and concatenates them into a single pandas DataFrame.
3. **Reproducibility**: Inside your script, strictly configure your numerical libraries to ensure exact reproducibility. Set the global random seed for numpy to `42`. Whenever a scikit-learn estimator or splitter requires a `random_state`, set it to `42`.
4. **Cross-Validation & Tuning**: 
   - The target variable is `target`. All other columns are features.
   - Build a scikit-learn `Pipeline` consisting of a `StandardScaler` and a `Ridge` regressor.
   - Use `GridSearchCV` with 5-fold cross-validation (`cv=5`, without shuffling) to tune the `alpha` parameter of the Ridge regressor. 
   - Search over the following `alpha` values: `[0.01, 0.1, 1.0, 10.0, 100.0]`.
   - Fit the GridSearchCV object on the entire concatenated dataset.
5. **Output Generation**:
   - Save the best hyperparameter and its corresponding mean cross-validation score to a JSON file at `/home/user/results.json`. The JSON should have exactly two keys: `"best_alpha"` (a float) and `"best_score"` (a float, rounded to 4 decimal places).
   - Use Large-scale data storage management principles by saving the entire concatenated pandas DataFrame to an HDF5 file at `/home/user/processed_data.h5` under the key `"dataset"` (use `format='table'` or `format='fixed'`, either is fine, but `pandas.DataFrame.to_hdf` is highly recommended).

Run your pipeline script so that `/home/user/results.json` and `/home/user/processed_data.h5` are generated.