You are tasked with fixing and optimizing a real-time sensor data processing pipeline. The system consists of multiple microservices that ingest large CSV files, perform dimensionality reduction, and generate diagnostic plots. Currently, the pipeline is broken and produces meaningless results and blank plots.

System Architecture (located in `/app/`):
1. **Redis**: Used as a message broker (expected on `localhost:6379`).
2. **Ingestion API** (`/app/api.py`): A FastAPI application running on port 8000 that accepts CSV rows via POST requests and pushes them to a Redis list named `sensor_stream`.
3. **Data Worker** (`/app/worker.py`): A Python daemon that pops data from Redis, performs dimensionality reduction (to 2 dimensions), saves the transformed data to `/home/user/reduced_data.csv`, and creates a scatter plot at `/home/user/cluster_plot.png`.

Your objectives:
1. **Fix the Multi-Service Configuration**: The worker is currently failing to connect to Redis due to a misconfigured environment variable `REDIS_PORT` in its startup script, and the API is not starting because it's missing the `uvicorn` dependency. Install necessary packages and ensure all three services (Redis, API, Worker) are running concurrently.
2. **Fix the Plotting Bug**: The `worker.py` script uses `matplotlib` to generate `cluster_plot.png`, but the resulting image is completely blank (0 bytes or just a white background). Modify `worker.py` to correctly generate and save the scatter plot in a headless Linux environment.
3. **Implement Reproducible Dimensionality Reduction**: The current worker naively selects the first two columns of the dataset as its "dimensionality reduction," which destroys the signal. You must rewrite the `process_batch` function in `worker.py`. It should:
   - Accumulate all incoming data.
   - Apply a `StandardScaler` followed by `PCA(n_components=2)` (from `scikit-learn`).
   - Fit the scaler and PCA pipeline ONLY on the first 1,000 rows, then transform the entire dataset (to ensure pipeline reproducibility simulating a streaming train/test split).
   - Save the transformed 2D dataset to `/home/user/reduced_data.csv` (header: `pc1,pc2`).
4. **Run the Pipeline**: We have provided a raw dataset at `/home/user/raw_sensors.csv` (10,000 rows, 50 features). You must write and run a script to POST all rows from this CSV to the API endpoint `http://127.0.0.1:8000/ingest` (which expects JSON: `{"features": [float, float, ...]}`). Wait for the worker to process all 10,000 rows.

**Verification:**
An automated test will evaluate your output using a quantitative metric. It will independently compute the canonical PCA transformation of `raw_sensors.csv` using the exact train/test split logic described above. The metric is the Mean Absolute Error (MAE) between your `/home/user/reduced_data.csv` and the canonical reference. 
To pass, your MAE must be strictly `< 0.01`, and `cluster_plot.png` must be a valid, non-blank image file larger than 15KB.