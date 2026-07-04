You are an ML engineer tasked with replacing a slow, legacy C++ feature extraction component with a fast machine learning surrogate model. 

We have a stripped binary located at `/app/legacy_extractor`. It takes exactly three floating-point numbers as command-line arguments and prints a single numerical feature to standard output.
Example: `/app/legacy_extractor 1.5 2.0 0.5`

Your objective is to:
1. **ETL & Data Storage:** Generate a dataset of 2,000 random samples (where x, y, z are uniformly distributed between 0.0 and 5.0). Run these through the `/app/legacy_extractor` to get the target labels. Store this generated dataset into an HDF5 file at `/home/user/training_data.h5` containing two datasets: `X` (shape 2000x3) and `y` (shape 2000).
2. **Model Training & Cross-Validation:** Train a scikit-learn model (e.g., RandomForestRegressor or GradientBoostingRegressor) to predict the binary's output given the three inputs. You must use cross-validation (e.g., `GridSearchCV`) to tune at least one hyperparameter (like `max_depth` or `n_estimators`). Save the best trained model to `/home/user/surrogate.pkl`. 
3. **Serving:** Write and run a Python HTTP web service using Flask or FastAPI that serves your trained model. 
   - The service MUST listen on `127.0.0.1:8000`.
   - It MUST expose a `POST` endpoint at `/predict`.
   - The endpoint will receive a JSON payload like: `{"x": 1.5, "y": 2.0, "z": 0.5}`.
   - It MUST return a JSON response with the predicted value: `{"prediction": 4.321}`.

Keep the service running in the background or foreground when you consider the task complete. The automated verifier will send requests to `http://127.0.0.1:8000/predict` and check if your surrogate model's predictions are sufficiently close to the actual binary's output (within 5% error).