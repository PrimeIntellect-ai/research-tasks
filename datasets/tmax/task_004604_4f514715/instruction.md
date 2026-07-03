You are tasked with cleaning a high-dimensional, noisy sensor dataset, identifying the most statistically significant latent features, and training a robust predictive model.

You have been provided with a custom, proprietary C++ extension with Python bindings for dimensionality reduction called `fastpca`. It is located at `/app/fastpca-1.2`. However, the package currently fails to build and install due to a misconfiguration in its setup files.

Your objectives are:

1. **Environment Setup (Vendored Package):**
   Fix the build configuration of the `/app/fastpca-1.2` package and install it in your Python environment. You will know it works when `import fastpca` succeeds.

2. **Dimensionality Reduction:**
   Load the training dataset `/app/data/train.csv`. The dataset contains 500 numeric feature columns (named `feature_0` to `feature_499`) and one binary target column (`target`). Separate the features and target.
   Use the fixed package to reduce the 500 features down to 20 components: `reduced_X = fastpca.reduce_dimensions(X.values, n_components=20)`.

3. **Bootstrap Confidence Intervals & Feature Selection:**
   You must filter these 20 latent components to remove statistical noise. For *each* of the 20 components, calculate the 95% empirical bootstrap confidence interval for its mean (using the percentile method with exactly 1000 resamples). 
   Select and retain *only* the components whose 95% confidence interval does **not** contain exactly `0.0`. Note the indices of these retained components.

4. **Cross-Validation & Hyperparameter Tuning:**
   Using *only* the retained components, train a machine learning classifier (e.g., Random Forest, Gradient Boosting, or SVM) to predict the `target`. You must use 5-fold cross-validation and hyperparameter tuning (e.g., via `GridSearchCV` or `RandomizedSearchCV`) to find an optimal model.
   Save your best fitted model (and any necessary scaler/indexer objects) to `/home/user/model_pipeline.pkl`.

5. **Integration (Prediction Script):**
   Write a standalone prediction script at `/home/user/predict.py`. It must accept exactly two command-line arguments:
   `python /home/user/predict.py <input_csv_path> <output_csv_path>`
   
   The script must:
   - Read the input CSV (which will have the same 500 feature columns but no `target` column).
   - Apply the `fastpca.reduce_dimensions` transformation.
   - Select the exact same component indices identified during training.
   - Use the loaded model from `/home/user/model_pipeline.pkl` to predict the probability of class `1`.
   - Write a CSV to `<output_csv_path>` containing a single column named `probability` with the predicted float values.

We will verify your solution by running your script against a hidden test set `/app/data/test.csv`. Your model must achieve a test ROC-AUC of at least 0.75.