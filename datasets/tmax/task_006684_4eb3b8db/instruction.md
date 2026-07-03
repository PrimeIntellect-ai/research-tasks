You are a web developer building a backend feature for a collaborative mathematics application. The system maintains a state file representing a numerical matrix, and clients update this matrix by sending standard unified diffs (patches). 

Your task is to implement the API endpoint that processes these patches, calculates specific numerical properties of the updated matrix, and returns the results. Finally, you will write an end-to-end test script to verify the workflow.

**Step 1: Complete the API Server**
An incomplete Python HTTP server is located at `/home/user/server.py`. 
Modify this file to fully implement the `POST /apply` endpoint. The endpoint must:
1. Read the raw POST request body, which will contain a standard unified diff.
2. Apply this unified diff to the file `/home/user/matrix.csv` using the standard Linux `patch` utility.
3. Parse the newly updated `/home/user/matrix.csv` (which contains comma-separated float values).
4. Implement numerical algorithms in Python to calculate two properties of the updated matrix:
   - **Trace**: The sum of the main diagonal elements.
   - **Frobenius Norm**: The square root of the sum of the absolute squares of all elements in the matrix.
5. Return a JSON response with status code 200 and the calculated values rounded to exactly 4 decimal places:
   `{"trace": <value>, "frobenius": <value>}`

*Note: You may use standard library Python modules only. Do not install external packages like NumPy or Flask.*

**Step 2: End-to-End Test Orchestration**
Create an executable bash script at `/home/user/e2e_test.sh`. This script must:
1. Start the API server (`/home/user/server.py`) in the background on port 8000.
2. Wait for the server to be ready (e.g., sleep for 1-2 seconds).
3. Use `curl` to send a POST request to `http://localhost:8000/apply` with the contents of `/home/user/test.patch` as the request body.
4. Save the exact HTTP response body to `/home/user/result.json`.
5. Gracefully terminate the background API server process.

When you are finished, run `/home/user/e2e_test.sh` to generate the `/home/user/result.json` file. We will verify your success by checking the contents of `/home/user/result.json` and the updated `/home/user/matrix.csv`.