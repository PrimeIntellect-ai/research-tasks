You are a Machine Learning Engineer tasked with preparing a training dataset for a customer churn model. Your data pipeline must pull real-time features from our internal microservices and join them with historical large-scale data storage.

However, the microservice stack is currently misconfigured. You need to fix the service configuration, start the stack, and then write the Python data pipeline.

### Part 1: Service Configuration
The data API stack consists of three services located in `/home/user/services/`:
1. **Redis**: Runs on port `6380`. Holds real-time session counters.
2. **Flask API**: An extraction service located in `/home/user/services/api/`. It should run on port `5000` and needs to connect to Redis.
3. **Nginx**: A reverse proxy located in `/home/user/services/nginx/`. It should listen on port `8080` and forward requests to the Flask API.

**Your objectives for Part 1:**
- Edit `/home/user/services/api/.env` to configure the correct `REDIS_URL`.
- Edit `/home/user/services/nginx/nginx.conf` to correctly `proxy_pass` to the Flask API.
- We have provided a script `/home/user/services/start_stack.sh` which starts Redis, Flask, and Nginx in the background. Fix the configs and run this script. Test that `curl http://localhost:8080/api/features` returns a JSON array of user records.

### Part 2: Data Pipeline
Write a Python script `/home/user/prepare_data.py` that performs the following steps:

1. **Multi-Source Joining**: 
   - Fetch the real-time JSON data from `http://localhost:8080/api/features`. Convert it to a Pandas DataFrame. It contains `user_id`, `session_duration`, `click_rate`, and `churn` (target variable).
   - Load the historical large-scale dataset from `/home/user/storage/historical.parquet`. It contains `user_id`, `transaction_volume`, and `support_tickets`.
   - Inner join the two datasets on `user_id`.

2. **Missing Value & Outlier Handling**:
   - `support_tickets` has missing values. Impute them using the median value of the column.
   - `transaction_volume` contains extreme outliers. Remove any rows where the `transaction_volume` is strictly greater than 3 standard deviations from its mean.

3. **Correlation & Dimensionality Reduction**:
   - `session_duration` and `click_rate` are highly correlated. Drop `click_rate` from the dataset entirely to prevent multicollinearity.
   - You are left with 3 feature columns: `session_duration`, `transaction_volume`, and `support_tickets`. 
   - Standardize these 3 feature columns (zero mean, unit variance).
   - Apply Principal Component Analysis (PCA) to reduce these 3 standardized features down to exactly 2 principal components (`pca_1`, `pca_2`).

4. **Storage Management**:
   - Create a final DataFrame containing exactly three columns in this order: `pca_1`, `pca_2`, and `churn`.
   - Save this DataFrame as a Parquet file at `/home/user/model_input.parquet`.

Make sure you run your script to generate the final `model_input.parquet` file. Our automated evaluation will train a logistic regression model on your output file to verify its predictive quality.