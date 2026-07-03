You are tasked with fixing a machine learning pipeline and deploying it as a microservice.

We have a video artifact located at `/app/experiment.mp4`. As a data analyst, your first step is to perform feature engineering by extracting frame-level statistics from this video to build a dataset. 
Specifically, you need to write a Python script that reads the video frame by frame and calculates two features for each frame (converted to grayscale):
1. `mean_brightness`: The average pixel intensity of the grayscale frame.
2. `std_brightness`: The standard deviation of the pixel intensity of the grayscale frame.

Save these features as a CSV file at `/home/user/features.csv` with columns: `frame_index`, `mean_brightness`, `std_brightness`. The `frame_index` should start at 0.

Next, you need to merge this data with our target variables located at `/app/targets.csv` (which contains `frame_index` and `target_value`).

We previously wrote a training script to predict `target_value` using Ridge Regression, but the model is currently suffering from data leakage. The previous analyst applied `sklearn.preprocessing.StandardScaler` to the entire dataset *before* performing cross-validation and splitting the data, resulting in artificially high CV scores. 

Your tasks:
1. Fix the data leakage by creating a proper `sklearn.pipeline.Pipeline` that chains the scaler and the Ridge regression model (`alpha=1.0`), ensuring that scaling is only fitted on the training folds.
2. Perform a 5-fold cross-validation on the merged dataset using this pipeline. Log the mean CV negative mean squared error to `/home/user/experiment_log.json` in the format: `{"cv_nmse": <float>}`.
3. Train the final pipeline on the *entire* merged dataset.
4. Deploy the trained pipeline as an HTTP web service using FastAPI or Flask. 
   - The service must listen on `127.0.0.1:8080`.
   - It must have an endpoint `POST /predict`.
   - The endpoint must accept a JSON payload like `{"mean_brightness": 100.5, "std_brightness": 25.0}`.
   - It must return a JSON response with the prediction, e.g., `{"prediction": 12.34}`.
   - Run the service in the background so that it remains active.

Ensure your service is up and running on `127.0.0.1:8080` before you finish, as an automated system will query the `/predict` endpoint to verify its correctness.