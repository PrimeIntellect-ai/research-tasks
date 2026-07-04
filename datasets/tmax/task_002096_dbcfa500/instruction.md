You are a platform engineer responsible for maintaining our CI/CD pipeline infrastructure. We have a lightweight mock CI server that serves test results to our dashboard, but the environment is currently broken.

Your task is to fix the dependencies, process the test results, and start the mock CI server.

Here is the situation:
1. We use a third-party C utility called `jo` to generate JSON payloads from shell scripts. The source code for `jo` version 1.9 is vendored at `/app/jo-1.9`. 
2. A recent bad merge broke the `Makefile.in` in the `jo` package, preventing it from compiling. You need to find the syntax error in `/app/jo-1.9/Makefile.in`, fix it, and build the `jo` binary (run `./configure && make`).
3. We have two partial test result files: `/app/test_results_A.txt` and `/app/test_results_B.txt`. Each contains key-value pairs (e.g., `unit=pass`).
4. You need to write a Bash script at `/home/user/start_server.sh` that starts an HTTP server listening on `0.0.0.0:8080`. 
5. The server must handle incoming HTTP `GET` requests to `/api/status`.
6. When a request is received, the server should:
   - Read both test result files.
   - Merge them and sort the keys alphabetically.
   - Use the compiled `jo` binary to construct a single JSON object representing the merged results.
   - Respond with a valid HTTP 1.1 `200 OK` response, including the header `Content-Type: application/json`, followed by the JSON body.

Run the server in the background or let it run in your final terminal session so it can be tested. Ensure your script is robust and uses standard bash tools (`nc` is available for the server loop).