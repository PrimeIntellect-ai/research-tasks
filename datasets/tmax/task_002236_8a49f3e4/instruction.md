You are a Machine Learning Engineer responsible for preparing training data for a new model. Our data pipeline is frequently polluted with anomalous "evil" data points that degrade model performance. Your goal is to create a robust data filter.

You have three main objectives:

1. **Environment Setup (Vendored Package):** 
   We have a proprietary data processing library located at `/app/datacleaner`. However, the previous maintainer left it in a broken state. It currently fails to install because of a nonexistent dependency listed in its `setup.py`. 
   - Locate the package at `/app/datacleaner`.
   - Fix the `setup.py` file to remove the invalid dependency (`broken-dep-123`).
   - Install the package in your Python environment.

2. **Cross-Validation and Modeling:**
   You are provided with a training dataset at `/home/user/train_data.csv`. This dataset contains three continuous features (`f1`, `f2`, `f3`) and a binary label `is_evil` (1 for anomalous data, 0 for clean data).
   - Write a script to explore this data and train a machine learning classifier (e.g., using `scikit-learn`'s `RandomForestClassifier` or `GradientBoostingClassifier`).
   - You must use cross-validation and hyperparameter tuning to ensure your model achieves 100% accuracy on the training data. Save your trained model to `/home/user/model.pkl`.

3. **Data Filter Implementation:**
   Create a script at `/home/user/filter.py` that acts as the final data sanitizer.
   - The script must accept two arguments: `--input` and `--output`.
   - Example invocation: `python /home/user/filter.py --input /path/to/input.csv --output /path/to/output.csv`
   - The script should load the model from `/home/user/model.pkl`.
   - It should read the CSV specified by `--input` (which will have `f1`, `f2`, `f3` but no labels).
   - It should use the `datacleaner` package's `clean_features` function (from `datacleaner.utils`) to preprocess the input features (e.g., `X_clean = clean_features(X_raw)`). Note: apply this same preprocessing to your training data before fitting the model!
   - It must predict which rows are "evil" (1) and which are "clean" (0).
   - The script must output a new CSV to the `--output` path containing **ONLY** the "clean" rows. The output CSV must retain the original header (`f1,f2,f3`).

Ensure your script is perfectly accurate, as it will be tested against hidden adversarial datasets.