You are a localization engineer managing an ETL pipeline that processes incoming translation updates. The system has been occasionally generating duplicate records on retry, so you need to redesign the pipeline to use an idempotent storage strategy, while correctly interpolating missing translation variables.

Your task is to build a robust localization processor using Bash.

**Step 1: Create the Transformation Logic**
Write a script at `/home/user/transform.sh` (make it executable) that reads exactly one JSON payload from standard input. 
The JSON has the following structure:
`{"msg_id": "...", "lang": "...", "template": "...", "vars": {"key1": "value1", "key2": ""}}`

Your script must:
1. Parse the JSON.
2. Replace all occurrences of `{key}` in the `template` string with the corresponding value from the `vars` dictionary.
3. **Imputation Rule:** If a variable is referenced in the template but its value in `vars` is an empty string `""` or the key is completely missing from `vars`, you must substitute it with the exact string `DEFAULT`.
4. Output a single line to standard output in this exact pipe-separated format:
   `msg_id|lang|interpolated_template`

Example Input:
`{"msg_id": "123", "lang": "fr", "template": "Bonjour {name}, you have {msgs} messages.", "vars": {"name": "Alice", "msgs": ""}}`

Example Output:
`123|fr|Bonjour Alice, you have DEFAULT messages.`

*Note: Your `transform.sh` will be subjected to rigorous randomized fuzz-testing against a reference binary to ensure it perfectly matches expected bit-exact behavior for all edge cases.*

**Step 2: Build the Orchestration Daemon**
Write a script at `/home/user/worker.sh` (make it executable) that acts as the pipeline DAG orchestrator and continuous worker.
1. Ensure a local `redis-server` is running on the default port (6379).
2. The script should run an infinite loop that continually consumes jobs from a Redis List named `loc_jobs` (e.g., using `BLPOP`).
3. For each JSON payload popped, pass it to `/home/user/transform.sh`.
4. To solve the duplicate records on retry issue, the worker must store the result idempotently. It should write the output to a Redis Hash named `loc_results`, where the hash field is the `msg_id` and the hash value is `lang|interpolated_template`.

**Step 3: Execution**
Start your `worker.sh` process in the background and leave it running. Ensure Redis is active. The automated test will push payloads to `loc_jobs` and inspect `loc_results`, as well as directly test `transform.sh`.