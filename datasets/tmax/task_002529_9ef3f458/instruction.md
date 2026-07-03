You are an AI data scientist tasked with cleaning a dataset, tuning a machine learning pipeline, and serving the results via a recommendation API. 

You have been provided with two files in the `/app/` directory:
1. `/app/data.csv`: A noisy dataset containing 12 columns: `id`, `f1` through `f10` (numeric features), and `target` (integer class labels). Some rows contain missing values (NaN or empty strings).
2. `/app/hyperparameters.png`: An image containing text that specifies the hyperparameter search grid and cross-validation settings for your pipeline.

Your task consists of the following steps:

1. **Information Extraction**:
   Extract the text from `/app/hyperparameters.png` (using Tesseract OCR or similar vision tools). The image contains three key-value pairs defining `CV_FOLDS`, `PCA_COMPONENTS` (a list of integers), and `K_NEIGHBORS` (a list of integers).

2. **Data Cleaning**:
   Read `/app/data.csv`. Remove any rows that contain missing or empty values in any column.

3. **Modeling & Hyperparameter Tuning**:
   Build a machine learning pipeline consisting of:
   - Standard scaling (mean=0, variance=1) of the features `f1` to `f10`.
   - Dimensionality reduction using Principal Component Analysis (PCA).
   - A K-Nearest Neighbors (KNN) classifier predicting the `target` variable.
   
   Perform a grid search cross-validation using the folds specified by `CV_FOLDS` and the parameter grids for `PCA_COMPONENTS` and `K_NEIGHBORS` extracted from the image. Evaluate the grid search using standard accuracy. Identify the best combination of PCA components and K neighbors. Retrain the pipeline on the full cleaned dataset using the best hyperparameters.

4. **API Serving**:
   Create and start an HTTP server listening on `127.0.0.1:8000`. You can use any framework (e.g., Flask, FastAPI, or standard library). 
   
   The server must expose a single endpoint:
   - **Method**: `POST`
   - **Path**: `/recommend`
   - **Payload**: JSON format, e.g., `{"features": [0.5, 1.2, -0.3, 0.0, 2.1, 1.1, -1.0, 0.5, 0.2, -0.8]}`
   - **Response**: A JSON object containing:
     - `"recommended_class"`: The predicted target class (integer) for the input features using the best pipeline.
     - `"similar_ids"`: A list of the `id`s of the `k` nearest neighbors from the cleaned dataset in the PCA-transformed space, where `k` is the best `K_NEIGHBORS` found. The IDs must be integers and ordered by distance (closest first).

Leave the server running in the background so that it can be queried by our automated verification system. Make sure the server binds to `127.0.0.1` and port `8000`.