You are a data scientist tasked with building a data pipeline and cleaning tabular data to train a predictive model. We have a multi-service setup located in `/app/` that needs to be configured and run.

There are three components:
1. A Redis instance that acts as a message broker and cache.
2. A Flask data ingestion API (provided in `/app/ingest_api/`).
3. A worker script you must create at `/home/user/pipeline/train_worker.py`.

Your tasks are:
1. **Service Configuration**: 
   - Start the Redis instance on port 6379.
   - Configure the Flask API in `/app/ingest_api/app.py` to connect to this Redis instance (the API currently has missing or incorrect connection details).
   - Start the Flask API on port 5000. 
   - Ensure the API successfully loads the raw dataset from `/app/data/raw_data.csv` into Redis under the key `dataset:raw`.

2. **Data Cleaning & Transformation**:
   - Write a script `/home/user/pipeline/train_worker.py` (you can use Python or any language you prefer, provided you install necessary dependencies) that retrieves the raw data from Redis.
   - Enforce the data schema: Ensure all feature columns (names starting with `feat_`) are numeric. Drop any rows with missing values or invalid data types.
   - Perform correlation analysis: Identify any pairs of features with an absolute Pearson correlation coefficient > 0.85. For each such pair, drop the feature that has the higher average absolute covariance with all other features.
   - The target column is `target`.

3. **Model Training & Evaluation**:
   - Train a regression model (e.g., Random Forest, Gradient Boosting, or Linear Regression) on the cleaned data.
   - Save the trained model predictions on a provided validation dataset located at `/app/data/val_features.csv`.
   - Your predictions must be saved as a CSV file at `/home/user/pipeline/predictions.csv` with a single column named `predicted_target`.
   
Your final model must achieve an R-squared ($R^2$) score of at least 0.75 on the validation set.