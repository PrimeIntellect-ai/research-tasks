You are an integration developer tasked with writing an automated Bash-based API testing suite. We have a local mock API server that simulates a complex, stateful workflow. You need to build a Bash script that acts as a state machine to navigate this API, transform data, and integrate the test into a simulated local CI/CD pipeline.

There is a Python mock API server located at `/home/user/mock_api.py`. 
First, start this server in the background using `python3 /home/user/mock_api.py &`. It listens on `http://127.0.0.1:8080`.

Next, write a Bash script `/home/user/state_tester.sh` that implements a state machine to interact with the API. You may install and use `jq` to parse the JSON responses.
The API has the following state flow:

1. **State: START**
   - Make a `GET` request to `http://127.0.0.1:8080/api/start`
   - Response format: `{"session_id": "...", "next_state": "AUTH", "challenge": "..."}`
   - Action: Extract `session_id`, `next_state`, and `challenge`.

2. **State: AUTH**
   - Action: Reverse the `challenge` string you received in the START state.
   - Make a `POST` request to `http://127.0.0.1:8080/api/auth` with a JSON body: `{"session_id": "<session_id>", "response": "<reversed_challenge>"}`
   - Content-Type must be `application/json`.
   - Response format: `{"token": "...", "next_state": "FETCH"}`

3. **State: FETCH**
   - Make a `GET` request to `http://127.0.0.1:8080/api/data`
   - You must include the header: `Authorization: Bearer <token>`
   - Response format: `{"items": [{"id": 1, "value": 10}, {"id": 2, "value": 25}, ...], "next_state": "SUBMIT"}`
   - Action: Parse the JSON array `items` and calculate the mathematical sum of all `value` fields.

4. **State: SUBMIT**
   - Make a `POST` request to `http://127.0.0.1:8080/api/submit` with a JSON body: `{"session_id": "<session_id>", "total_value": <sum_calculated>}`
   - Content-Type must be `application/json`.
   - Response format: `{"status": "success", "next_state": "DONE", "flag": "<secret_flag>"}`

Your script `/home/user/state_tester.sh` should execute this state machine loop until it reaches the `DONE` state. Upon reaching `DONE`, it must print ONLY the `<secret_flag>` to standard output. Ensure the script is executable.

Finally, set up a local CI hook:
1. Create a `Makefile` at `/home/user/Makefile`.
2. Add a target named `test-api` to the `Makefile` that runs `/home/user/state_tester.sh` and redirects its standard output to `/home/user/ci_output.log`.

Execute the `test-api` target in your `Makefile` so the log file is generated.