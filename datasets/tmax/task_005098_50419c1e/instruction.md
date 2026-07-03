You are a data engineer tasked with building a validation and ETL ingestion pipeline. We've been experiencing "data leakage" where downstream machine learning models achieve suspiciously perfect scores because the target variable `y` was accidentally duplicated as a feature column in `X`. We also have issues with perfectly multicollinear features causing our linear models to fail due to singular matrices.

Your objective is to build a robust Python sanitiser and configure the ingestion services.

**Step 1: Bring up the Multi-Service Ingestion Backend**
The backend consists of three cooperating services that you must configure and start:
1. **Redis**: Needs to run on the default port `6379`.
2. **Flask Ingestion API**: Located at `/app/services/api.py`. It runs on port `5000` and depends on Redis.
3. **Nginx Reverse Proxy**: A configuration file is provided at `/app/services/nginx.conf`. You must configure Nginx to listen on port `8080` and proxy requests to the Flask API on port `5000`. Start Nginx using this configuration.

**Step 2: Build the Data Sanitiser**
Write a Python script at `/home/user/sanitiser.py`.
The script will be invoked as: `python /home/user/sanitiser.py <path_to_json_file>`

The input JSON file contains a dictionary with two keys:
- `"X"`: A 2D list of floats (the feature matrix).
- `"y"`: A 1D list of floats (the target vector).

Your script must perform linear algebra validations:
1. **Multicollinearity Check**: Compute the matrix $X^T X$. If its determinant is strictly less than `1e-4`, the data is invalid.
2. **Target Leakage Check**: Check if the target vector `y` is linearly dependent on *any single column* of `X` (e.g., if `y` is identical to a column in `X` or a scaled version of it, within a tolerance of `1e-4` for the correlation coefficient being exactly 1 or -1, or simply check if the absolute Pearson correlation between `y` and any column of `X` is $> 0.9999`). If so, the data is invalid.

**Behavior**:
- If the data is **invalid** (evil), the script MUST exit with status code `1` and not send any data.
- If the data is **valid** (clean), the script MUST send the original JSON payload as a POST request to `http://localhost:8080/ingest` with the `Content-Type: application/json` header. If the POST request is successful (HTTP 200), the script MUST exit with status code `0`.

Ensure the services are running and your script handles both clean and evil data correctly. You can test your logic manually, but the final evaluation will run your script against hidden datasets.