You are an ML engineer tasked with preparing training data, training a baseline predictive model, and deploying it as a microservice. Our infrastructure relies on a custom, internal experiment tracking library called `fast-tracker`, which was recently vendored into the environment but is currently failing to build. 

Your objectives are as follows:

1. **Fix and Install the Vendored Package:**
   Our internal package, `fast-tracker` (version 1.0.0), is located at `/app/fast-tracker-1.0/`. It contains a C-extension for fast math operations. Currently, running `make` and installing it fails due to a configuration perturbation in its `Makefile`. Identify the issue, fix the `Makefile`, compile the package, and install it into your Python environment.

2. **Data Preparation and Correlation Analysis:**
   You have a dataset located at `/home/user/dataset.csv`. The dataset contains several continuous numerical features (`f1`, `f2`, ..., `f15`) and a continuous `target` column.
   Write a Python script that uses `pandas` and `numpy` to calculate the Pearson correlation matrix for the features (excluding the `target`). 
   Identify highly collinear features: if any pair of features has an absolute correlation > 0.85, drop the feature that comes later in the alphabetical order (e.g., if `f3` and `f7` are highly correlated, drop `f7`).
   Save the filtered dataset to `/home/user/filtered_dataset.csv`.

3. **Experiment Tracking and Model Training:**
   Using the fixed `fast-tracker` package, initialize a tracking run.
   Train a Ridge Regression model (`sklearn.linear_model.Ridge`, default parameters, `random_state=42`) using the filtered dataset to predict the `target`.
   Use `fast-tracker.log_metric("mse", <value>)` to log the Mean Squared Error of the model on the training set.
   Save the trained model to `/home/user/model.pkl` using `joblib`.

4. **Serve the Model:**
   Create and start a web service (using Flask or FastAPI) listening on exactly `127.0.0.1:8080`.
   The service must expose the following endpoints:
   - `GET /metrics`: Returns a JSON object containing the tracked MSE, e.g., `{"mse": 12.34}`.
   - `POST /predict`: Accepts a JSON payload containing an array of feature values for the *filtered* features, e.g., `{"features": [1.2, 3.4, ...]}`. It must return the Ridge model's prediction as JSON: `{"prediction": 5.67}`.
   
The service must run continuously and be accessible by our automated evaluation suite. Ensure the service handles requests appropriately.