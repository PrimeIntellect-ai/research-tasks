You are an expert Data Scientist and ML Engineer. Your task is to build a robust data cleaning, training, and inference pipeline. 

We have a proprietary Python package called `datacleaner` vendored at `/app/datacleaner-1.2.0`. However, it has a bug: its internal schema enforcement module fails to properly drop rows with invalid integer formats in the `age` column, instead returning them as NaN. 
First, identify the bug in `/app/datacleaner-1.2.0/datacleaner/schema.py`, fix it so that rows with non-castable integers in the `age` column are entirely dropped from the dataframe, and install the fixed package locally.

Second, construct an ETL script that reads a raw dataset from `/home/user/data/raw_users.csv`. Use the fixed `datacleaner` package to enforce the schema. Perform basic feature engineering: encode the `category` column using one-hot encoding, and fill missing values in the `income` column with the median. Train a simple Random Forest classifier on the cleaned dataset to predict the `is_active` target variable.

Finally, you must deploy the trained model and data cleaning pipeline as a web service. 
Create a FastAPI (or Flask) application that listens on `127.0.0.1:8000`. 
It must expose an endpoint `POST /predict` that accepts a JSON payload containing an array of raw user records. The endpoint must require an authorization header `Bearer secret-token-99X`.
The endpoint should process the records using your ETL pipeline, run inference, and return a JSON array of predictions. 
Write your service script to `/home/user/serve.py` and start it in the background.

Before finishing, benchmark your inference API using a script to ensure it can handle at least 50 concurrent requests. Log your benchmarking results to `/home/user/benchmark_results.txt`.