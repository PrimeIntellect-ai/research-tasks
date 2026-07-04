You are a data engineer tasked with fixing and completing an ETL and model-training pipeline. 

We have a local microservice architecture consisting of two APIs:
1. **Data Source API**: Runs on port `8000`. Endpoint `http://localhost:8000/raw_data` returns a raw CSV file containing user telemetry data (`id`, `age`, `income`, `activity_score`, `target`).
2. **Model Training API**: Runs on port `8001`. Endpoint `http://localhost:8001/train` accepts a POST request with a CSV file (form field `file`) and trains a predictive model, saving it to `/home/user/model.joblib`.

Currently, the services are provided in `/app/services/`. You must start them. However, they might need slight configuration adjustments (e.g., ensuring they bind to the correct ports or setting the `MODEL_SAVE_PATH` environment variable so the training API writes to `/home/user/model.joblib`).

Your main goal is to write a robust Bash script at `/home/user/run_pipeline.sh` that performs the following ETL workflow:
1. **Extract**: Fetch the raw data from the Data Source API.
2. **Transform** (using `awk`, `sed`, `jq`, or standard GNU coreutils):
   - The raw data has an issue: empty `income` fields silently cause column shifts or parse as `NaN` in downstream pandas, ruining the model. You must filter out any rows missing the `target` or `id` fields.
   - For missing `age` values, impute them with the integer median of the valid `age` values.
   - Handle outliers in `income`: Remove any rows where `income` is strictly greater than 300,000 (these represent test-account anomalies).
   - Compute the Pearson correlation between `activity_score` and `target` using a small inline tool or awk script, and write this single float value to `/home/user/correlation.txt`.
3. **Load / Train**: Submit the cleaned CSV to the Model Training API via `curl`. 

Requirements:
- Your script `/home/user/run_pipeline.sh` must be executable and run the end-to-end process autonomously.
- The downstream model's performance relies heavily on your data cleaning. Your goal is to achieve an Root Mean Squared Error (RMSE) of **less than 12.5** on the Model Training API's internal validation set. The API will return a JSON response with the RMSE when you submit the file.
- Do not use Python for the Extract and Transform steps; you must use Bash and standard Linux text processing utilities.

Deliverables:
- A configured and running service environment.
- The pipeline script at `/home/user/run_pipeline.sh`.
- The extracted correlation written to `/home/user/correlation.txt`.
- The compiled model saved at `/home/user/model.joblib` (triggered via the API).