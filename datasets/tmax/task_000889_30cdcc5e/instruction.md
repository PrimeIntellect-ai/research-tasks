You are helping a researcher organize and analyze a multi-modal dataset consisting of sensor metadata and audio recordings. The researcher has started a workflow but left several broken scripts and unlinked data sources. 

Your objective is to complete the data pipeline, train a predictive model, fix a plotting script, and serve the model via a web API.

Here are your specific tasks:

1. **Audio Feature Extraction & Dimensionality Reduction**:
   There is an audio file at `/app/subject_recordings.wav` containing exactly 100 consecutive 1-second audio segments (total duration: 100 seconds). 
   - Using Python (e.g., `librosa` or `scipy`), extract the 13 Mel-frequency cepstral coefficients (MFCCs) for each 1-second segment. Compute the mean of each of the 13 MFCCs over the 1-second window. You should end up with a 100x13 feature matrix (one row per second/subject).
   - Apply Principal Component Analysis (PCA) to reduce these 13 features down to exactly 2 principal components (`pca_1` and `pca_2`). Do not scale the MFCCs before PCA.

2. **Data Joining & Cleaning**:
   - Load the metadata from `/app/subject_metadata.csv`. This file has 100 rows corresponding to the 100 audio segments (IDs 0 to 99 in order).
   - Join the 2 PCA features to this dataset.
   - **Outlier Handling**: Remove any subjects (rows) where the `heart_rate` column is greater than 150.
   - **Missing Values**: The `age` column has missing values. Impute them using the median `age` of the *remaining* (non-outlier) dataset.

3. **Classification Modeling**:
   - Using the cleaned dataset, train a Logistic Regression model to predict the `diagnosis` column (which is binary: 0 or 1).
   - Use `pca_1`, `pca_2`, `age`, and `heart_rate` as your four predictor features (in that exact order). Use default hyperparameters for the Logistic Regression model in `scikit-learn` (no scaling required before this step).

4. **Fix the Visualization**:
   - The researcher wrote a script at `/app/plot_clusters.py` to plot the PCA components, but it currently fails or produces a blank/empty image because the matplotlib backend is misconfigured for a headless Linux environment.
   - Modify the script so it successfully runs and outputs a valid PNG image at `/home/user/pca_clusters.png`. You must plot `pca_1` on the X-axis and `pca_2` on the Y-axis.

5. **Serve the Model (API)**:
   - Create and run a web server (e.g., using FastAPI or Flask) listening on `127.0.0.1:8080`.
   - Implement a `GET /ping` endpoint that returns a JSON response: `{"message": "pong"}`.
   - Implement a `POST /predict` endpoint that accepts a JSON payload with keys: `pca_1`, `pca_2`, `age`, `heart_rate`. It should use your trained model to return the prediction as JSON: `{"prediction": <0_or_1>}`.
   - Keep the server running in the background or terminal so it can be queried.

Ensure all tasks are executed successfully. The automated verifier will test your API endpoints and check the generated plot.