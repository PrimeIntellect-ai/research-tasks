Hello! We have a legacy proprietary scoring engine that generates 4-dimensional embeddings for text descriptions. Currently, it's just a compiled, stripped binary located at `/app/scorer_bin`. As a data analyst, I need to integrate this into a modern data processing pipeline. 

I need you to build a Python-based HTTP REST API that acts as a processing gateway. The server must run continuously and listen on `127.0.0.1:5000`.

Here are the requirements for the system:

1. **Database Setup**:
   Create a SQLite database at `/home/user/data.db`. It should have a table named `records` with the following columns: 
   `id` (INTEGER PRIMARY KEY), `category` (TEXT), `description` (TEXT), `metric` (REAL), `emb_0` (REAL), `emb_1` (REAL), `emb_2` (REAL), `emb_3` (REAL).

2. **Schema Enforcement & Processing**:
   Implement a `POST /upload` endpoint that accepts a `multipart/form-data` upload with a single file field named `file`. The file will be a CSV with a header row: `id,category,description,metric`.
   For each row in the CSV, enforce the following strict schema:
   - `id`: Must be a valid integer.
   - `category`: Must be exactly one of: 'ALPHA', 'BETA', 'GAMMA'.
   - `description`: Must be a non-empty string.
   - `metric`: Must be a valid float greater than or equal to 0.0.
   
   If a row fails *any* of these validation rules, skip that row entirely (do not process or save it).
   For valid rows, execute the binary `/app/scorer_bin` passing the `description` as a single command-line argument (e.g., `/app/scorer_bin "some text"`). The binary prints exactly four space-separated floats to standard output. 
   Save the validated row data along with these four embedding floats into the SQLite database.

3. **Data Retrieval**:
   Implement a `GET /record/<id>` endpoint that returns a JSON response for the given integer ID. 
   If the record exists, return HTTP 200 with the JSON format:
   `{"id": 123, "category": "ALPHA", "description": "some text", "metric": 1.5, "embedding": [0.1, 0.2, 0.3, 0.4]}`
   If the record does not exist, return HTTP 404 with JSON: `{"error": "Not found"}`.

4. **Execution**:
   Write your application using any standard Python web framework (like Flask or FastAPI - you can install them using pip). Start the server in the background so it remains running. The automated test will send HTTP requests to verify your schema logic, binary integration, and database storage.

Please provide a robust solution that handles the processing efficiently!