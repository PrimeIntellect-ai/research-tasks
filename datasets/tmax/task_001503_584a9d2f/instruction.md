You are an engineer setting up an automated polyglot test orchestrator from scratch. Our testing architecture requires testing multiple language modules (Python, Node.js, C++) by querying a central test coordinator via WebSockets, evaluating the test execution formulas it returns, and comparing the results against legacy benchmarks.

Your objective is to write a bash script `/home/user/polybuild/orchestrate.sh` that fully automates this end-to-end test orchestration. 

We have provided a workspace at `/home/user/polybuild` containing:
1. `build_server.py`: A Python WebSocket server listening on `ws://localhost:9090`.
2. `ws_client.py`: A Python WebSocket client script. Run it as `python3 ws_client.py "<MESSAGE>"` to send a message to the server and print the response to stdout.
3. `legacy_results.txt`: A CSV file containing legacy build scores in the format `TASK_ID,LEGACY_SCORE`.

Your script `/home/user/polybuild/orchestrate.sh` must perform the following actions:
1. Start `build_server.py` in the background and wait for it to be ready on port 9090.
2. Use `ws_client.py` to send the exact string `"GET_TEST_TASKS"` to the server.
3. Capture the server's response. The response is a custom data structure where each line represents a test task in the format: `TASK_ID;;MATH_EXPRESSION;;MODULE_NAME`.
4. Parse the response. For each line, extract the `MATH_EXPRESSION` and mathematically evaluate it (e.g., using `bc`). This evaluates to the `CURRENT_SCORE`.
5. Create a sorted, merged, and diffed report. You must merge your calculated `CURRENT_SCORE`s with the `LEGACY_SCORE`s found in `legacy_results.txt` by matching the `TASK_ID`.
6. Calculate the difference for each task: `SCORE_DIFF = CURRENT_SCORE - LEGACY_SCORE`.
7. Generate the final output file at `/home/user/polybuild/diff_report.txt` with the format `TASK_ID,SCORE_DIFF`.
8. The final `diff_report.txt` must be sorted alphabetically by `TASK_ID`.
9. Ensure you cleanly kill the background `build_server.py` process before your script exits.

Constraints:
- You must write your orchestration logic in Bash.
- You may use standard Linux command-line utilities (`bc`, `awk`, `sort`, `join`, `grep`, etc.).
- The `orchestrate.sh` script must have execute permissions.

When you are done, just run your `orchestrate.sh` script to ensure it creates the `/home/user/polybuild/diff_report.txt` correctly.