You are a data scientist taking over a project from a departed colleague. They left behind a compiled Linux binary at `/app/legacy_score_predictor` which represents a proprietary scoring model. The source code is lost, and the binary has been stripped of debug symbols.

You have a raw training dataset at `/home/user/train_data.csv` and a test dataset at `/home/user/test_data.csv`. Both files contain 10 raw features (columns `A` through `J`), which are messy and contain formatting issues or missing values.

Your task is to:
1. **Analyze the binary** `/app/legacy_score_predictor` to determine what inputs it expects (hint: it requires exactly 3 specific, cleaned features from the dataset).
2. **Perform feature engineering and data cleaning** on `/home/user/train_data.csv` to extract and prepare the features the binary requires.
3. **Query the binary** using your cleaned training data to generate the ground-truth scores for the training set. 
4. **Train a surrogate machine learning model** (using Python or your language of choice) to predict the score directly from the raw or cleaned data.
5. **Predict the scores** for `/home/user/test_data.csv` using your trained surrogate model.
6. **Save the predictions** to `/home/user/predictions.csv`.

Requirements for `/home/user/predictions.csv`:
- It must be a headerless CSV file containing exactly one column of floating-point numbers (the predicted scores).
- The number of rows must exactly match the number of rows (excluding the header) in `/home/user/test_data.csv` (500 rows).
- The row order must be preserved.

Your solution will be evaluated by an automated script that compares your predictions against the true outputs of the binary on the test set. You must achieve a Mean Squared Error (MSE) of less than 0.1.