You are assisting a release manager in setting up a pre-flight deployment verification tool. 

Your task is to implement a C library that parses deployment requests using a state machine, validates them, and enforces a rate limit. Then, you must build a test fixture to verify its behavior.

1. Create a header file `/home/user/deploy.h` with the following signature:
   `int process_deploy_request(const char* request);`

2. Implement this function in `/home/user/deploy.c`. 
   - The function must parse an incoming request string using a simple state machine.
   - The expected format is strictly: `[TOKEN] DEPLOY <target>@<version>`
     - `[TOKEN]` is an alphanumeric string (max 16 chars).
     - `<target>` is an alphanumeric string (max 16 chars).
     - `<version>` is a string starting with 'v' followed by digits and dots (e.g., `v1.2.3`).
     - There is exactly one space between `[TOKEN]` and `DEPLOY`, and one space between `DEPLOY` and `<target>@<version>`.
   - **Validation**: If the request does not exactly match this format, return `400`.
   - **Rate Limiting**: The system must track requests per `[TOKEN]` in memory. A token is allowed a maximum of 2 validly formatted requests. If a correctly formatted request is received for a token that has already made 2 requests, return `429`. 
   - If the request is perfectly formatted and within the rate limit, return `200`.

3. Write a test fixture in `/home/user/test_deploy.c`. This file must include `deploy.h` and contain a `main` function that tests the `process_deploy_request` function with the following sequence of requests in order:
   1. `"ALPHA1 DEPLOY backend@v1.0.0"`
   2. `"ALPHA1 DEPLOY backend@v1.0.1"`
   3. `"ALPHA1 DEPLOY backend@v1.0.2"`
   4. `"BETA2 BADCMD frontend@v2"`
   5. `"BETA2 DEPLOY frontend@v2.1.0"`
   6. `"ALPHA1 DEPLOY backend@v1.0.3"`

4. The test fixture must write the results of these calls to a log file at `/home/user/test_results.log`. The file should contain exactly six lines, corresponding to the return codes of the six test cases, in the following format:
   ```
   Test 1: <RETURN_CODE>
   Test 2: <RETURN_CODE>
   Test 3: <RETURN_CODE>
   Test 4: <RETURN_CODE>
   Test 5: <RETURN_CODE>
   Test 6: <RETURN_CODE>
   ```

5. Compile your code using `gcc -o /home/user/run_tests /home/user/deploy.c /home/user/test_deploy.c` and execute `/home/user/run_tests` to generate the log file.