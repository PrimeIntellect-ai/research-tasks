You are helping a mathematical data researcher prepare a dataset of mathematical expressions and test it against a mock evaluation model. Your goal is to tokenize the data, calculate numerical ground truths, enforce a data schema, run a mock model inference, and build a reproducible bash pipeline.

There is a raw dataset located at `/home/user/raw_math.jsonl`. Each line is a JSON object with keys `id` (integer) and `expr` (string, a space-separated mathematical expression).

Your task has 4 parts:

**1. Data Processing and Tokenization**
Read `/home/user/raw_math.jsonl`. For each line:
- Parse the `expr` string. 
- Calculate the true mathematical numerical value of the expression (as a float).
- Tokenize the `expr` string by splitting it by spaces.
- Map each token to an integer ID using the following exact vocabulary mapping:
  `+`: 0, `-`: 1, `*`: 2, `/`: 3, `(`: 4, `)`: 5, `0`: 6, `1`: 7, `2`: 8, `3`: 9, `4`: 10, `5`: 11, `6`: 12, `7`: 13, `8`: 14, `9`: 15, `.`: 16.
*(Assume all tokens in the dataset are present in this vocabulary).*

**2. Data Schema Enforcement**
Write the processed data to a new file at `/home/user/processed_dataset.jsonl`.
Each line must be a valid JSON object matching exactly this schema:
- `id`: integer
- `tokens`: list of strings (the space-separated characters)
- `token_ids`: list of integers (the mapped vocabulary IDs)
- `true_value`: float (the evaluated mathematical result)

**3. Model Architecture Reconstruction & Numerical Accuracy Testing**
The researcher has a mock linear embedding model used for testing pipeline integrations. You must reconstruct its inference logic in Python.
The model predicts a value for an expression as follows:
- `Prediction = sum(W[token_id]) + bias` (where the sum is over all `token_ids` in the expression).
- `W` is an array of weights where `W[i] = 0.15 * i` for `i` in range 0 to 16.
- `bias` is `1.5`.

Run this mock inference on every item in `processed_dataset.jsonl`. 
Calculate the Mean Squared Error (MSE) across the entire dataset:
`MSE = average( (Prediction - true_value)^2 )`

Save the final MSE to `/home/user/metrics.json` in the following format:
`{"mse": <float>}` (Keep the float unrounded).

**4. Reproducible Pipeline**
Create an executable bash script at `/home/user/run_pipeline.sh` that, when executed, runs your Python script to read the raw data, generate the processed dataset, and produce the `metrics.json` file. 

You may create any intermediate Python files you need in `/home/user/`.