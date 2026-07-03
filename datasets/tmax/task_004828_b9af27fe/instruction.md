You are an AI assistant helping a localization engineering team fix and deploy a data validation service. 

We have a partially built translation validation server located at `/app/loc-server/`. The service receives translation updates as JSON-Lines via HTTP POST requests, validates them, and calculates summary statistics. The server is primarily written in Bash, utilizing `socat` for networking and standard shell utilities (`jq`, `awk`) for data processing.

Unfortunately, the previous engineer left behind two issues:
1. **Unicode/JSON Escape Bug**: The service currently crashes or calculates incorrect lengths when encountering Unicode escape sequences (e.g., `\u3042`) or multi-byte UTF-8 characters. 
2. **Missing Logic**: The constraint validation and rolling aggregation logic are incomplete.

Your task is to fix the scripts in `/app/loc-server/` and start the server so it correctly processes incoming translation streams.

### Server Requirements:
* The server must listen on `127.0.0.1:8080`.
* It must accept HTTP POST requests containing a JSON-Lines body. 
* Each line in the body will be a JSON object with the following schema:
  `{"id": "<string>", "text": "<string>", "max_chars": <integer>}`
* The `text` field may contain raw UTF-8 characters or JSON Unicode escape sequences.

### Processing Logic to Implement:
For a given HTTP POST request body (a batch of JSON-lines), process the lines in order:
1. **Decode and Measure:** Determine the true length of the `text` field in **Unicode characters** (not bytes). 
2. **Constraint Validation:** A line is considered *valid* if the character length of `text` is less than or equal to `max_chars`. Otherwise, it is *invalid*.
3. **Summary Statistics:** Calculate the total number of valid lines, the total number of invalid lines, and the overall average character length of all *valid* lines.
4. **Rolling Aggregation:** Calculate the average character length of the **last 3** *valid* lines processed in the current batch. If fewer than 3 valid lines exist, calculate the average of however many are available.
5. **Output Format:** The server must respond with an HTTP 200 OK containing exactly the following JSON structure (formatted as a single line or pretty-printed):
  ```json
  {
    "valid_count": <integer>,
    "invalid_count": <integer>,
    "avg_valid_len": <float>,
    "rolling_avg_3": <float>
  }
  ```
  *(Note: Floats should be formatted to 2 decimal places, e.g., `4.00`, `3.33`).*

### Existing Files in `/app/loc-server/`:
* `start.sh`: A script that runs `socat` to listen on port 8080 and pipe requests to `handle_req.sh`.
* `handle_req.sh`: Extracts the HTTP body and pipes it to `process_data.sh`.
* `process_data.sh`: A Bash script meant to parse the JSON, apply the logic, and output the result. 

Review and modify `process_data.sh` (and any other files if necessary) to fix the Unicode handling and implement the missing logic. Once fixed, execute `./start.sh &` to run the service in the background. Leave the service running.