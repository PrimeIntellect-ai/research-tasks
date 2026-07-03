You are assisting a machine learning researcher in organizing and cleaning up a large repository of tabular datasets for a new automated ML pipeline. The researcher has set up a "Data Curator Portal" to automate dataset ingestion, but the system is currently broken and the data sanitization logic is missing.

The portal consists of three services running locally:
1. **Nginx** (serves static dataset files on port 8080).
2. **Redis** (used as a job and metadata queue on port 6379).
3. **Flask API** (the main controller, supposed to run on port 5000).

Your objective is to fix the pipeline, implement a robust data leakage detector, and verify the system works end-to-end.

**Step 1: Fix the Multi-Service Pipeline**
The source code for the Flask API is located at `/home/user/portal/app.py`. 
Currently, if you start the services, the Flask API fails to process requests because it is misconfigured. 
- You need to fix the environment variables or hardcoded configuration in `/home/user/portal/app.py` so that it connects to Redis on the correct local port (6379) instead of the erroneous default it currently has.
- It also attempts to fetch datasets from Nginx using the wrong internal URL. Fix it to fetch from `http://127.0.0.1:8080/datasets/`.
- Once fixed, start the services by running the provided script: `bash /home/user/portal/start_services.sh`.

**Step 2: Implement the Data Leakage Detector**
The Flask API relies on an external Python script to validate datasets. You must create this script at `/home/user/sanitizer.py`.
The script will be invoked by the API as: `python3 /home/user/sanitizer.py <dataset_directory>`

A `<dataset_directory>` will contain two files: `train.csv` and `test.csv`. 
Your script must load these files and detect two specific types of data leakage:
1. **Row Overlap:** Check if there are any exact duplicate rows between `train.csv` and `test.csv`. When comparing rows, you MUST ignore the `id` and `target` columns (if they exist). Only compare the feature columns.
2. **Target Leakage (Correlation):** In `train.csv`, compute the Pearson correlation coefficient between every numerical feature column and the `target` column. If the absolute value of the correlation for any feature is `>= 0.99`, it is considered target leakage.

If *either* type of leakage is detected, the script must print EXACTLY the string `LEAK_DETECTED` to standard output and exit with code `1`.
If the dataset is perfectly valid and has no leakage, the script must print EXACTLY the string `CLEAN` to standard output and exit with code `0`.

**Step 3: Verification Integration**
To prove your setup works, use `curl` to trigger the Flask API for a test dataset.
Run the following command and save the output to `/home/user/integration_test.log`:
`curl -X POST http://127.0.0.1:5000/analyze -H "Content-Type: application/json" -d '{"dataset_id": "test_sample"}'`

Ensure your `sanitizer.py` handles missing values appropriately (e.g., by dropping them or using a robust correlation calculation) and relies only on standard data science libraries (pandas, numpy, scikit-learn).