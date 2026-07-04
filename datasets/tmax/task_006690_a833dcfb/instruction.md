You are a platform engineer maintaining CI/CD pipelines. We have a legacy Node.js step in our pipeline that connects to a local build agent via WebSockets to fetch and evaluate dynamic resource limit constraints. 

Unfortunately, the legacy script (`/home/user/legacy/fetch_limits.js`) fails our static security scans because it uses the insecure `eval()` function to calculate the mathematical expressions sent by the build agent server. This exposes our pipeline to arbitrary code execution (RCE) vulnerabilities.

Your task is to translate this JavaScript WebSocket client into a secure Python script located at `/home/user/fetch_limits.py`.

Requirements:
1. The new Python script must replicate the WebSocket protocol flow seen in the legacy JavaScript code: connect to `ws://localhost:9999`, receive a JSON-encoded list of mathematical expressions, evaluate them, send back a JSON-encoded list of the numerical results, and then close the connection.
2. **Security Constraint:** You **MUST NOT** use Python's `eval()`, `exec()`, or any similar unsafe dynamic execution functions. You must implement or use a safe expression parser to evaluate the arithmetic expressions. The expressions will only contain integers and the operators `+`, `-`, `*`, `/`, and parentheses `()`.
3. You may use the standard `ast` module to safely parse and evaluate the syntax tree, or write your own evaluator.
4. The `websockets` Python library is available in the environment. 

The mock build agent server is already running in the background on `localhost:9999`. Once you have written `/home/user/fetch_limits.py`, execute it. If your script behaves correctly and securely evaluates the expressions, the local build agent server will verify the answers and automatically write a success token to `/home/user/result.txt`. 

Your goal is to successfully generate `/home/user/result.txt`.