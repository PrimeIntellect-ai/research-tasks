You are an open-source maintainer reviewing a recent Pull Request for your scheduling project located in `/home/user/scheduler-pr`. 

The PR introduces a new WebSocket-based scheduling service in `/home/user/scheduler-pr/server.py`. The service is supposed to listen on `ws://127.0.0.1:8765`, accept incoming JSON payloads containing tasks and workers, and calculate a valid assignment. 

However, the CI tests are failing. The PR author made several mistakes:
1. The WebSocket communication crashes because it tries to send a raw Python dictionary instead of a JSON string.
2. The constraint satisfaction logic is flawed: it does not enforce that a worker can only be assigned to a **single** task. It currently assigns the first worker with the required skill to multiple tasks.
3. The PR entirely missed a requirement: every valid response sent back to a client (whether assignments or an error) must be appended as a JSON string on a new line to `/home/user/scheduler_log.jsonl`.

**Payload Specification:**
Incoming JSON format:
```json
{
  "tasks": [
    {"id": "t1", "required_skill": "python"},
    {"id": "t2", "required_skill": "bash"}
  ],
  "workers": [
    {"id": "w1", "skill": "bash"},
    {"id": "w2", "skill": "python"}
  ]
}
```

Expected Response format (if all tasks can be assigned):
```json
{
  "assignments": [
    {"task_id": "t1", "worker_id": "w2"},
    {"task_id": "t2", "worker_id": "w1"}
  ]
}
```
*Note: If it is impossible to assign exactly one uniquely skilled worker to every task, the server must respond with exactly:* `{"error": "unsatisfiable"}`

**Your Task:**
1. Fix the bugs in `/home/user/scheduler-pr/server.py` so that it correctly parses the structured data, satisfies the 1-to-1 worker-to-task skill constraints, formats the JSON correctly, and logs every response to `/home/user/scheduler_log.jsonl`.
2. Install any necessary Python packages (the PR uses the `websockets` library).
3. Start the server in the background so it is actively listening on `127.0.0.1:8765`.