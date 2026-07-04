You are a data scientist tasked with cleaning a corrupted sensor dataset, loading it into a database, and serving the cleaned data via a REST API.

1. **Dataset Handling**: You have a raw dataset at `/app/raw_sensor_data.jsonl`. Each line is a JSON object with `id`, `messy_log`, and `readings` (an array of numbers with `null` values).
2. **Text Normalization**: For each record, tokenize and normalize the `messy_log` field: convert to lowercase, remove all non-alphanumeric characters (except spaces), and split by whitespace into a list of words.
3. **Imputation**: For the `readings` array, you must use the provided proprietary stripped binary located at `/app/imputer_oracle`. The binary takes a single command-line argument: a space-separated string of the readings (using `NaN` for `nulls`). It will print the fully imputed space-separated values to standard output.
4. **Database Import**: Bulk load the cleaned data into an SQLite database at `/app/cleaned_sensors.db` with a table named `sensor_data` (columns: `id` INTEGER PRIMARY KEY, `tokens` TEXT (JSON serialized), `readings` TEXT (JSON serialized)).
5. **API Service**: Write and run a Python web service (e.g., using Flask or FastAPI) that exposes this database.
   - It must listen on `127.0.0.1:8080`.
   - It must require an `Authorization` header with the exact value: `Bearer secret_impute_token_99`.
   - Endpoint: `GET /api/record/{id}` should return a JSON response: `{"id": <id>, "tokens": [<list of strings>], "readings": [<list of floats>]}`.
   - Endpoint: `POST /api/export` should bulk export the database to a CSV file at `/app/export.csv` and return `{"status": "success"}`.

Start the web service in the background and write a log file to `/app/service_ready.log` containing the text "READY" once the service is actively listening.