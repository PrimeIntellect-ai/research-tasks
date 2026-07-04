You are a localization engineer managing a translation ingestion pipeline. Our system allows translators to upload CSV files containing translated UI strings. However, we've encountered issues with malformed files (specifically, rows with unquoted embedded newlines that break our parsers) and malicious input (invalid interpolation markers that cause frontend crashes).

Your task is to fix the translation backend and implement a robust CSV sanitizer.

### Part 1: Service Composition
Our ingestion pipeline uses Nginx as a reverse proxy, a Flask API for processing, and Redis for storage. The startup script `/home/user/app/start_services.sh` launches these, but they are misconfigured.
1. Configure Nginx (`/home/user/app/nginx.conf`) to listen on port 8080 and route requests for `/api/` to the Flask app running on `127.0.0.1:5000`.
2. Configure the Flask app (`/home/user/app/app.py`) to properly connect to Redis (running on `127.0.0.1:6379`) using the `REDIS_HOST` and `REDIS_PORT` environment variables.

### Part 2: CSV Sanitization and Imputation
Implement the core logic in `/home/user/app/sanitizer.py`. The file must contain a function with the following signature:
`def process_translations(upload_csv_path: str, base_csv_path: str) -> pd.DataFrame:`

This function must:
1. Read both the uploaded translation CSV and the base English CSV (`base_csv_path`). Both use `|` as a delimiter.
2. **Merge & Impute:** Join the uploaded translations with the base English strings on the `string_id` column. If a translation is missing or empty in the uploaded CSV, impute it using the base English string.
3. **Filter Malformed/Evil Input:** The uploaded strings often contain broken formatting. You must drop rows from the resulting DataFrame if the translation string contains:
   - Unquoted embedded newlines (you must cleanly drop the row without crashing the CSV parser).
   - Forbidden HTML tags (specifically `<script>` or `<iframe>`).
   - Mismatched interpolation braces (e.g., string contains `{user` but no closing `}`).

### Part 3: Stratified Sampling
Add a second function to `/home/user/app/sanitizer.py`:
`def write_stratified_sample(df: pd.DataFrame, output_json_path: str):`
This function must take the cleaned DataFrame, group it by the `context_tag` column, randomly sample exactly 2 rows per context (or 1 if only 1 exists), and export the result to the provided JSON file path.

Ensure the system is running and the Python script correctly implements the pipeline. You can test your logic using the files located in `/home/user/test_data/`.