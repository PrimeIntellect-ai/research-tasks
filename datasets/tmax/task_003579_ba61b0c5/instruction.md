You are assisting a researcher in organizing and analyzing a large-scale dataset. We have a multi-service architecture running locally: a PostgreSQL database containing the raw sensor data, a Redis cache for fast model parameter storage, and a Rust-based processing service that you need to fix.

Currently, the PostgreSQL service is running on `127.0.0.1:5432` (database: `sensordb`, user: `researcher`, password: `password123`). The Redis instance is running on `127.0.0.1:6379`. 

In `/home/user/app`, there is a Rust project. The application is meant to:
1. Connect to PostgreSQL and Redis (you need to configure the connection string in `/home/user/app/.env`).
2. Fetch the large training dataset from the `training_data` table (columns: `feature_1`, `feature_2`, `feature_3`, `target`).
3. Compute the correlation between each feature and the target variable.
4. Select the single feature with the highest absolute correlation.
5. Compute the simple linear regression weights (slope and intercept) for this chosen feature.
6. Store these weights in Redis (keys: `model:best_feature`, `model:slope`, `model:intercept`).
7. Read the `test_data` table, predict the target using the stored model, and write the predictions to `/home/user/predictions.csv` (format: `id,predicted_target`).

Your task is to:
1. Create the `/home/user/app/.env` file and correctly glue the services together.
2. Complete the `src/main.rs` file where marked `TODO: IMPLEMENT CORRELATION, COVARIANCE, AND REGRESSION LOGIC`.
3. Run the Rust application to generate the predictions.

The output will be evaluated automatically by comparing `/home/user/predictions.csv` against the ground truth target values in the test set. Your model must achieve a Mean Squared Error (MSE) of strictly less than 2.0.

Ensure your code handles the data accurately and successfully connects all services.