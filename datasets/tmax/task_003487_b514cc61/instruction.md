You are a data engineer migrating a legacy log processing pipeline to a new real-time microservice. 

Your task is to create a Python HTTP web service that acts as a real-time ETL pipeline. It must receive raw log events, transform and normalize the data, validate it against strict constraints, and return the processed result.

Here are the requirements for your service:

1. **Server Configuration:**
   - Must listen on `127.0.0.1:8000`.
   - Must accept `POST` requests to the `/process` endpoint.

2. **Input Data Format:**
   - The endpoint will receive a JSON payload with two fields: `timestamp` (a string in various formats) and `message` (a raw log string).
   - Example Input: `{"timestamp": "2023-10-25 08:30:00 EST", "message": "User admin failed to LOGIN. Code: 401"}`

3. **Transformation 1: Timestamp Alignment**
   - Parse the input `timestamp`. It could be in formats like `YYYY-MM-DD HH:MM:SS TZ` (e.g., EST, PST, UTC) or ISO 8601.
   - Convert it to a strict UTC ISO 8601 string in the format: `YYYY-MM-DDTHH:MM:SSZ`.

4. **Transformation 2: Tokenization & Normalization**
   - There is a proprietary, compiled legacy tokenizer located at `/app/legacy_tokenizer`. 
   - This stripped binary reads a single line of text from Standard Input (stdin) and outputs a normalized, space-separated string of tokens to Standard Output (stdout).
   - You must pass the `message` field through this binary to get the normalized tokens. 

5. **Transformation 3: Constraint-based Validation**
   - After tokenization, evaluate the following constraints to determine if the log is "valid":
     - Constraint A: The normalized token string must contain the token `err` or `fail`.
     - Constraint B: The total number of tokens output by the binary must be greater than 3.
   - If both constraints are met, the log is valid. Otherwise, it is invalid.

6. **Output Data Format:**
   - Return a JSON response with HTTP status 200.
   - The JSON response must have exactly the following fields:
     - `utc_time`: The aligned ISO 8601 timestamp string.
     - `normalized_message`: The exact string output by the `/app/legacy_tokenizer` binary.
     - `is_valid`: A boolean indicating if the constraints were met.
   - Example Output: `{"utc_time": "2023-10-25T13:30:00Z", "normalized_message": "user admin fail login code 401", "is_valid": true}`

Start the server in the background or foreground when you are done. The automated test will send HTTP requests to `127.0.0.1:8000/process` to verify your implementation. You may install Python packages like `Flask` or `python-dateutil` if needed.