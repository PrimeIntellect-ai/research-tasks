You are an engineer tasked with modernizing a legacy algorithmic tool. We have a Go library that computes the Levenshtein distance between two strings, but it currently has a bug in its dynamic programming implementation. Additionally, we need to expose this algorithm as a REST API and ensure it is fully tested for a minimal container deployment.

Your objectives:

1. **Fix the Algorithm**: 
   In `/home/user/app/distance.go`, the `Levenshtein(a, b string) int` function is incorrect. Rewrite or fix it to correctly compute the standard Levenshtein distance (insertion, deletion, and substitution costs are all 1).

2. **Implement the REST API**:
   Modify `/home/user/app/main.go` to start an HTTP server on port 8080. 
   It must implement the following endpoint:
   - **Path**: `/api/v1/levenshtein`
   - **Method**: `POST`
   - **Request Body** (JSON): `{"str1": "<string1>", "str2": "<string2>"}`
   - **Response Body** (JSON): `{"distance": <integer>}`
   - Return HTTP 400 Bad Request if the JSON is invalid or missing fields.

3. **Write Unit Tests**:
   Create `/home/user/app/distance_test.go` and write unit tests for the `Levenshtein` function. Include at least these pairs:
   - "kitten" and "sitting" (distance 3)
   - "flitten" and "flitten" (distance 0)
   - "" and "abc" (distance 3)
   Run `go test -v ./... > /home/user/unit_tests.log`.

4. **End-to-End Test Orchestration**:
   Write a bash script `/home/user/app/e2e_test.sh` that:
   - Starts the Go server in the background.
   - Waits for the server to be ready.
   - Uses `curl` to make a POST request to the API with `str1`="book" and `str2`="back".
   - Captures the HTTP response body and writes it exactly to `/home/user/e2e_results.json`.
   - Cleans up and kills the background server.
   Run the script to generate `/home/user/e2e_results.json`.

Ensure your Go code compiles and formats correctly. The final verification will check the test log, run the API, and inspect the JSON outputs.