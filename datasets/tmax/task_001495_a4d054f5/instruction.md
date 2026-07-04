You are acting as a DevOps engineer troubleshooting a Go-based state reconciler tool. 

The tool is located in the Git repository at `/home/user/reconciler`. It is supposed to read desired configuration states from a local SQLite database, update an in-memory state representation concurrently, and write the final converged state to a file. 

However, the tool is currently broken in several ways:
1. **Authentication Failure**: The tool requires an environment variable `SECRET_TOKEN` to run. A previous developer temporarily hardcoded this token in the Go code, but later removed it in a past commit. You need to find this secret token in the git history and set it as the `SECRET_TOKEN` environment variable before running the tool.
2. **Race Condition**: When run, the tool often panics with a "concurrent map writes" error. You need to modify the Go code to fix this concurrency bug so that the goroutines can safely update the state map.
3. **Query Bug**: The SQL query inside the Go code fetches all configuration items, including inactive ones. You must fix the query so it only retrieves items where the `active` column is equal to `1`.
4. **Convergence Failure**: The reconciler runs in a loop, continually trying to converge. However, due to a bug in how it verifies the applied state against the desired state, it fails to recognize when it has successfully converged and loops infinitely (or panics). Fix the convergence check in the Go code.

Once you have fixed the Go code and recovered the secret token, compile and run the tool. When it completes successfully, it will automatically generate a file at `/home/user/converged_state.json`.

To complete the task, fix the Go program, build it, run it with the correct `SECRET_TOKEN`, and ensure that `/home/user/converged_state.json` is created with the correct final state. Finally, output the value of the `SECRET_TOKEN` into `/home/user/token.txt`.