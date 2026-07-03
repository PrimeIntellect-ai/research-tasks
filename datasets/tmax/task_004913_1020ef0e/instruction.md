You are tasked with setting up a local experiment tracking environment and writing a robust data cleaning and processing pipeline for telemetry data.

Your objectives are divided into two parts: Service Configuration and Data Processing.

**Part 1: Service Configuration (Environment Setup & Experiment Tracking)**
We have two background services that need to be running for the broader data platform to function:
1. A Redis cache server.
2. A custom Flask-based experiment tracking API located at `/app/tracker_api.py`.

Currently, these services are not running or configured properly. 
- You must configure and start a local Redis server on the default port (6379).
- You must start the experiment tracking API. It requires an environment variable `REDIS_HOST=127.0.0.1` and `TRACKER_PORT=8080` to run properly. Run it in the background. 
- Ensure both services are actively listening on their respective ports (6379 and 8080) on localhost.

**Part 2: Data Processing Pipeline (Fuzz Equivalence)**
You must write a Python script at `/home/user/process.py` that acts as a deterministic data cleaner and statistical calculator. Our continuous integration system will test your script against a reference binary by feeding it thousands of randomized JSON inputs via standard input (`stdin`). Your script's standard output (`stdout`) must match the reference exactly, byte-for-byte.

**Script Requirements (`/home/user/process.py`):**
1. Read a single JSON payload from `stdin`. The JSON will have the following structure:
   ```json
   {
     "users": [{"user_id": 1, "age": 25}, {"user_id": 2, "age": -5}, ...],
     "events": [{"user_id": 1, "clicks": 10, "time": 1.5}, {"user_id": 3, "clicks": 5, "time": 0.2}, ...]
   }
   ```
2. **Schema Enforcement & Cleaning**:
   - Filter `users`: Keep only users where `user_id` is an integer, `age` is an integer, and `age` >= 0.
   - Filter `events`: Keep only events where `user_id` is an integer, `clicks` is an integer, `clicks` >= 0, and `time` is a number (float or int) >= 0.
   - Ignore any objects missing these exact keys or having invalid types.
3. **Data Joining**:
   - Inner join the cleaned `users` and `events` on `user_id`. If a `user_id` appears multiple times in `users` or `events`, take the *first* valid occurrence in the respective list.
4. **Statistical Analysis**:
   - Calculate the Pearson correlation coefficient between the `age` and `clicks` for the joined dataset.
   - If the number of joined records is less than 2, or if the standard deviation of either `age` or `clicks` is 0 (which makes correlation undefined), the correlation should be represented as a JSON `null`.
5. **Output**:
   - Print a single JSON string to `stdout` with exactly this format (no extra whitespace, printed via `json.dumps(..., separators=(',', ':'))`):
     `{"valid_joined_records":<integer>,"correlation":<float rounded to 4 decimal places or null>}`
   - Example valid output: `{"valid_joined_records":2,"correlation":0.9543}` or `{"valid_joined_records":1,"correlation":null}`

Do not print any debugging information or logs to stdout. Only the final JSON string should be printed.