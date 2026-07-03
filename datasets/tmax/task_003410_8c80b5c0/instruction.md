You are a data engineer tasked with fixing and improving a machine learning ETL pipeline. 

We have a multi-service architecture running locally. 
In the `/app` directory, there is a `docker-compose.yml` file that defines two services:
1. A PostgreSQL database (port 5432) containing our training data.
2. A Redis cache (port 6379) containing metadata features.

Your tasks are:
1. **Start the Services**: Bring up the PostgreSQL and Redis services using the provided docker-compose file. Wait a few seconds for them to be fully initialized. The Postgres credentials are user: `admin`, password: `secret`, database: `etl_db`.
2. **Fix the ETL Bug**: Look at `/app/pipeline.py`. It extracts data from Postgres (`documents` and `labels` tables), queries Redis for an author's reputation score, concatenates text and reputation features, trains a model, and makes predictions. However, the model performance is currently terrible. There is a silent data type conversion bug in pandas caused by missing values that corrupts the Redis lookups. Identify and fix this issue so the pipeline correctly retrieves author reputations.
3. **Enhance the Model**: The current pipeline uses a basic classifier with default parameters. Modify `/app/pipeline.py` to include cross-validation and hyperparameter tuning (e.g., using `GridSearchCV`) to find better hyperparameters for the model before making final predictions.
4. **Generate Predictions**: The pipeline script currently generates a file `/home/user/test_predictions.csv` based on `/app/test_documents.csv`. Ensure your fixed and improved pipeline writes the final predictions to `/home/user/test_predictions.csv` with exactly two columns: `id` and `label`.

Do not modify the test dataset. Focus entirely on fixing the ETL feature extraction bug and implementing proper hyperparameter tuning to maximize your model's accuracy. A successful run will be evaluated based on the F1-score of your predictions against a hidden ground truth.