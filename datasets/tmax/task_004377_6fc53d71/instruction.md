You are a data engineer tasked with fixing a buggy Bash-based ETL and prediction pipeline. 

We have a dataset located at `/app/data.csv` containing 1000 rows and 3 comma-separated numerical columns (`X1`, `X2`, `X3`). 
We also have a pre-trained linear model, but its weights are stored in an image file: `/app/weights.png`.

Currently, our junior engineer created a pipeline that suffers from **data leakage**: it normalizes the entire dataset (computing the global mean and standard deviation) before splitting it into training and testing sets. 

Your task is to build a reproducible pipeline entirely in Bash (using standard tools like `awk`, `bc`, `sed`, etc., and `tesseract` for OCR) that corrects this data leakage and computes predictions for the test set.

Here are your exact requirements:
1. **Extract Weights:** Read the 3 weights (W1, W2, W3) from `/app/weights.png` using Tesseract OCR. The image contains a single line of text with three space-separated numbers.
2. **Train/Test Split:** Treat the first 800 rows of `/app/data.csv` as the training set, and the remaining 200 rows as the testing set.
3. **Fix Data Leakage (Standardization):** 
   - Calculate the mean and population standard deviation (using N=800, not N-1) for `X1`, `X2`, and `X3` exclusively on the **training set**.
   - Standardize the **testing set** using the mean and standard deviation calculated from the training set. Formula: `X_norm = (X - mean_train) / std_train`. If a standard deviation is 0, do not divide by 0 (assume it's 1, though our data won't have 0 variance).
4. **Linear Algebra Prediction:** For each row in the standardized testing set, compute the predicted value `Y_pred` as the dot product of the weights and the standardized features: `Y_pred = W1 * X1_norm + W2 * X2_norm + W3 * X3_norm`.
5. **Output:** Save the 200 predicted values to `/home/user/predictions.txt`. The file should contain exactly 200 lines, with one numeric prediction per line, corresponding to rows 801-1000 of the original dataset.

Write your entire fixed pipeline in `/home/user/run_pipeline.sh` and execute it. Your final predictions will be evaluated against a reference implementation.