We are experiencing issues with our configuration management ETL pipeline. Network retries have caused duplicate configuration records to be ingested into our system, and we need a streaming deduplication service to process the logs and maintain the correct current state.

Please build a Python-based HTTP server that fulfills the following requirements:

1. **Authentication & Rules Extraction**: 
   There is an image file located at `/app/auth_schema.png`. You must extract the text from this image (e.g., using `tesseract`). It contains two critical pieces of information:
   - A secret token used for authentication.
   - The name of the primary key field that you must use to identify duplicate records.

2. **HTTP Service**:
   Create a Python HTTP server listening exactly on `127.0.0.1:8080`. It must expose two endpoints:
   
   - **`POST /ingest`**: 
     - This endpoint will receive streaming text payloads of JSON Lines (JSONL). 
     - It MUST require an `Authorization: Bearer <secret_token>` header. If the token is missing or incorrect, return a 401 Unauthorized status.
     - Process the JSONL payload. Each line is a JSON object representing a configuration change.
     - **Deduplication Logic**: Use the primary key field extracted from the image to track records. If multiple records share the same primary key, keep only the record with the highest integer `timestamp` field.
     - **Logging**: For every duplicate record that is discarded (i.e., an older or equal timestamp record), append its exact raw JSON string to a log file at `/home/user/dropped.log` (one JSON object per line).
     - Return a 200 OK status when the payload is successfully processed.

   - **`GET /state`**:
     - Returns a 200 OK status with a single JSON object representing the current configuration state.
     - The JSON object should map the primary key values to their active `config_value` fields. 
     - Example response body: `{"item_A": "enabled", "item_B": "disabled"}`.

You may use standard Python libraries or install lightweight frameworks like Flask/FastAPI if you prefer. Keep the server running in the foreground or background once started so it can be evaluated by our automated verification pipeline.