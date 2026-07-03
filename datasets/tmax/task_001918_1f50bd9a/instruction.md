You are an AI assistant helping a data scientist automate a dataset cleaning and serving pipeline.

You have been provided with two input files:
1. `/app/raw_data.csv`: A raw dataset containing four columns: `id`, `category`, `raw_text`, and `value`.
2. `/app/pipeline_config.png`: An image of a whiteboard containing essential configuration parameters for the pipeline. You must use OCR (e.g., `tesseract`, which is installed) to read this image.

Your task is to build a Python-based pipeline that processes the data and serves the results via a local HTTP API.

**Step 1: Extract Configuration**
Read the text from `/app/pipeline_config.png`. The image contains a configuration string that specifies three parameters:
- `STRATA_SIZE` (an integer)
- `WINDOW` (an integer for rolling statistics)
- `CRON` (a cron schedule expression)

**Step 2: Data Cleaning and Processing**
Create a Python script that reads `/app/raw_data.csv` and performs the following operations:
1. **Unicode Normalization**: The `raw_text` column contains multi-language text with inconsistent unicode representations. Normalize all text in this column to the `NFKC` unicode form.
2. **Rolling Statistics**: Sort the dataset by `id` in ascending order. Then, calculate a rolling mean on the `value` column using a window size equal to the `WINDOW` extracted from the image. Use a minimum period of 1 (so the first few rows just average the available data). Create a new column called `rolling_avg` for these values.
3. **Stratified Sampling**: Using the `category` column, take a stratified sample where you select exactly `STRATA_SIZE` rows per category. Specifically, take the *first* `STRATA_SIZE` rows for each category based on the `id` sorting.
4. Save this processed dataset as a JSON list of records to `/home/user/cleaned_data.json`.

**Step 3: Service Setup**
Write and start a Python HTTP server (e.g., using FastAPI, Flask, or `http.server`) that listens on `127.0.0.1:8000`. The server must:
1. Enforce authentication: All requests must include the HTTP header `Authorization: Bearer ds_secret_token`. Return a 401 Unauthorized status if missing or incorrect.
2. Expose the endpoint `GET /api/data`: Returns the contents of `/home/user/cleaned_data.json` with a 200 OK status.
3. Expose the endpoint `GET /api/config`: Returns a JSON object with the configuration extracted from the image: `{"cron": "<extracted_cron_string>", "strata_size": <extracted_int>, "window": <extracted_int>}`.

**Step 4: Cron File**
Write the extracted cron schedule into a plain text file at `/home/user/cron_schedule.txt` so that a system administrator can easily review it later. The file should just contain the cron string.

Make sure your HTTP service is running in the background before completing the task.