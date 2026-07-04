You are an MLOps engineer tasked with recovering a lost experiment artifact and serving it via a reproducibility tracking API.

A previous engineer generated a plot summarizing a model's run but lost the original metadata file. The plot image is located at `/app/experiment_summary.png`. Tesseract OCR is installed on your system.

**Stage 1: Metadata Recovery**
Extract the text from `/app/experiment_summary.png`. It contains critical experiment metadata, specifically:
- Experiment ID
- Random Seed
- Alpha level (significance level)
- Baseline Accuracy

**Stage 2: Data Schema Enforcement & Modeling**
You have a dataset at `/app/dataset.csv`.
1. Clean the dataset: drop any rows with missing values (NaN), and drop any rows where the `target` column is not strictly `0` or `1`.
2. Train a `RandomForestClassifier` on the cleaned dataset. Use the exact Random Seed extracted from the image as the `random_state`. Leave all other hyperparameters at their default values.
3. Evaluate the model using 10-fold cross-validation (`cross_val_score`). Calculate the mean accuracy of the 10 folds.

**Stage 3: Hypothesis Testing**
Perform a 1-sample, right-tailed t-test to determine if the cross-validated accuracies are significantly greater than the Baseline Accuracy extracted from the image. 
An experiment is considered "reproducible" if the p-value is less than the Alpha extracted from the image, AND the mean accuracy is strictly greater than the Baseline Accuracy.

**Stage 4: Reproducibility Tracking API**
Create an HTTP REST API listening on `127.0.0.1:8080`. The API must require an `Authorization` header in the format `Bearer <Experiment ID>` (using the ID extracted from the image). If the auth header is missing or incorrect, return a `401 Unauthorized`.

Implement two endpoints:
1. `GET /metadata`
   Returns a JSON payload with the extracted parameters:
   ```json
   {
     "seed": <int>,
     "alpha": <float>,
     "baseline": <float>
   }
   ```

2. `GET /test-reproducibility`
   Runs the modeling and hypothesis testing pipeline dynamically and returns:
   ```json
   {
     "mean_accuracy": <float>,
     "p_value": <float>,
     "reproducible": <boolean>
   }
   ```

Ensure your server remains running in the background or foreground so it can be verified. Write the API in Python using Flask or FastAPI.