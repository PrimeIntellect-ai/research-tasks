You are an engineer completing a new web feature for a calculator application. The project uses a multi-language microservice architecture. You need to fix a dependency issue, implement an expression parser, configure a reverse proxy, and write an end-to-end test.

All your work should take place in `/home/user/calc-feature`.

Phase 1: Node.js Service (Expression Parsing & Bug Fix)
Inside `/home/user/calc-feature/nodejs-svc`, there is a Node.js project. 
1. When you try to run `npm install`, it fails due to a conflicting peer dependency between a custom local plugin and `express`. Fix the `package.json` or use an appropriate npm flag to successfully install the dependencies.
2. The `server.js` file contains an endpoint `POST /evaluate`. It accepts a JSON body: `{"expression": "..."}`. You must complete the implementation inside `server.js` to parse and evaluate the mathematical expression string. The expression will contain integers, spaces, and the operators `+`, `-`, `*`, `/`, and parentheses `()`. Standard order of operations applies. Do not use `eval()` or external math libraries (like `mathjs`) for the evaluation—implement a custom parsing algorithm (e.g., Shunting Yard or recursive descent).
3. Ensure the service runs and listens on port 3001. It should return JSON: `{"result": <number>}`.

Phase 2: Reverse Proxy Configuration
You need to set up an Nginx reverse proxy to route traffic to the Node.js service and an existing Python service (located in `/home/user/calc-feature/python-svc`, which runs on port 3002).
1. Create an Nginx configuration file at `/home/user/calc-feature/nginx.conf`.
2. Configure Nginx to listen on port 8080.
3. Route requests matching `/api/calc` to the Node.js service (`http://127.0.0.1:3001`).
4. Route requests matching `/api/status` to the Python service (`http://127.0.0.1:3002`).
5. Since you do not have root access, configure Nginx to run as the current user. Use `/home/user/calc-feature/nginx_run/` for Nginx's pid, logs, and client body temp paths so it doesn't try to write to `/var/log` or `/run`.

Phase 3: End-to-End Test Orchestration
1. Ensure both services and the Nginx reverse proxy are running.
2. Write a test script at `/home/user/calc-feature/run_e2e.py`.
3. The script should send an HTTP GET request to `http://127.0.0.1:8080/api/status`.
4. The script should send an HTTP POST request to `http://127.0.0.1:8080/api/calc/evaluate` with the JSON payload: `{"expression": "10 + 2 * (6 - (4 / 2))"}`.
5. The script must capture the responses and write them to a file named `/home/user/calc-feature/e2e_results.json` in the following exact format:
```json
{
  "status_response": <parsed JSON response from /api/status>,
  "calc_response": <parsed JSON response from /api/calc/evaluate>
}
```

Run your E2E script and leave the `e2e_results.json` file on disk for verification. You do not need to leave the background services running after generating the final JSON file.