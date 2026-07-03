You are an ETL data engineer taking over a broken machine learning pipeline. 

We have a local multi-service architecture simulating our production environment. There are two services:
1. A Data API (Flask) running on port 5000, which serves the training data.
2. A Redis instance running on port 6379, acting as our intermediate feature cache.

To start the services, run:
`/app/start_services.sh`

In your home directory, there is a script `/home/user/etl_pipeline.py`. It is supposed to:
1. Fetch a JSON dataset of product listings from `http://127.0.0.1:5000/data`. The data contains `description` (text), `category` (categorical), and `price` (numerical target).
2. Compute TF-IDF features followed by TruncatedSVD for the `description`.
3. Compute Target Encoding for the `category` (mean of `price` per category).
4. Train a Ridge regression model to predict `price`.
5. Cache the final pipeline components or intermediate steps in Redis (currently failing due to misconfiguration).
6. Save the final model pipeline to `/home/user/final_pipeline.pkl`.

However, the current script has two major issues:
1. **Service Disconnection:** It fails to connect to the Redis service correctly and does not fetch data properly from the API.
2. **Data Leakage:** The author applied `fit_transform` on the entire dataset for both the SVD/TF-IDF step and the Target Encoding step *before* splitting the data into train and test sets. This causes severe data leakage, leading to an artificially low Mean Absolute Error (MAE) during local evaluation, but it will fail completely in production.

**Your Task:**
1. Start the background services.
2. Fix `/home/user/etl_pipeline.py` so that it correctly retrieves data from the Data API and stores a dummy key `pipeline_status: success` in Redis to prove connectivity.
3. Completely rewrite the data processing steps using `sklearn.pipeline.Pipeline` and `sklearn.compose.ColumnTransformer` (or meticulously careful manual splits) to strictly prevent any data leakage between the training and testing phases. The transformations (TF-IDF, SVD, Target Encoding) must ONLY be fitted on the training set (80% of the data).
4. Save the corrected, fitted `sklearn` pipeline object (which must be capable of taking raw inference data and returning predictions) to `/home/user/final_pipeline.pkl`.

We will evaluate your saved pipeline on a hidden, held-out dataset using a rigorous evaluation script. Your model must achieve a real Test MAE of less than 45.0 on this hidden set.