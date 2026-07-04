You are tasked with fixing a regression in a Bash-based sensor aggregation service. The service receives batches of high-precision floating-point readings over TCP, aggregates them, and returns the result. Recently, a regression was introduced that causes precision loss and an off-by-one error (dropping the last sensor reading in the format parsing).

You have two main objectives:

1. **Find the Regression**: 
   A local Git repository at `/home/user/sensor_repo` contains the service (`server.sh`). There are exactly 200 commits. The commit tagged `v1.0` is known to be good, and the `master` branch is currently broken. Use `git bisect` to identify the exact commit hash that introduced the precision loss and off-by-one parsing error. Write this single Git commit hash to `/home/user/bad_commit.txt`.

2. **Fix and Deploy the Service**:
   Check out the `master` branch and fix `server.sh` so that it correctly parses all floats and computes the sum without precision loss.
   
   Because Bash cannot handle floating-point arithmetic natively without precision loss, you have been provided with a stripped, compiled binary at `/app/kahan_oracle`. This black-box binary takes space-separated floats as command-line arguments and outputs the highly accurate sum to standard output. You should use this binary in your fixed `server.sh` script to handle the summation.

   Once fixed, you must start the service in the background so it can be verified. 
   
   **Service Specifications:**
   *   **Listen Address:** `127.0.0.1:8888` (TCP).
   *   **Connection handling:** The server must handle multiple sequential client connections (e.g., using `socat`).
   *   **Protocol:**
       1. The client connects and sends an authentication line: `AUTH: v2_auth_token_xyz`
       2. If the token is correct, the server must reply exactly with: `AUTH_OK\n`
       3. If the token is incorrect, the server must reply `AUTH_FAIL\n` and close the connection.
       4. After successful authentication, the client sends a data line: `DATA: 1.000001 2.000002 3.000003 ...`
       5. The server must parse the floats, pass them to `/app/kahan_oracle`, and return the result as: `RESULT: <oracle_output>\n`. The server should then close the connection.

Ensure your fixed server is running and listening on port 8888 before you finish the task.