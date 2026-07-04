I am reviewing a Pull Request for our new multi-language expression evaluation microservice. The contributor attempted to build a WebSocket server that evaluates mathematical and logical expressions in different programming languages based on the connection URL. 

However, the PR is broken and doesn't meet our specifications. Here is how the system *should* work:

1. **WebSocket Server**: Runs on port `8080`.
2. **URL Routing**: Clients should be able to connect to `ws://localhost:8080/eval/<language>`, where `<language>` is exactly one of `python`, `ruby`, or `node`. If the route doesn't match this pattern or the language is not supported, the server must reject the WebSocket upgrade (close the socket).
3. **Expression Evaluation**: 
   - The client sends a JSON message like: `{"expr": "2 + 3 * 4"}`.
   - The server parses this expression and safely evaluates it in the specified language.
   - The server must respond with a JSON message containing the natively typed result: `{"result": 14}` (Note: it must be a JSON number/boolean, NOT a string).
4. **Current State**: The contributor's code is in `/home/user/app/server.js`. It has bugs in URL parsing, command execution (it currently returns strings instead of typed results), and doesn't restrict the languages properly.

**Your Task:**
1. Fix the server implementation in `/home/user/app/server.js`.
2. Ensure the server is running in the background.
3. Write a test script at `/home/user/run_tests.py` that connects to your running server and evaluates the following expressions:
   - Python (`/eval/python`): `"max(10, 20) * 2"`
   - Ruby (`/eval/ruby`): `"15 % 4 == 3"`
   - Node (`/eval/node`): `"Math.pow(2, 3) + 1"`
4. Your test script must save the responses in a single JSON dictionary to `/home/user/results.json` mapping the language to its evaluated result, exactly like this:
   ```json
   {
     "python": 40,
     "ruby": true,
     "node": 9
   }
   ```