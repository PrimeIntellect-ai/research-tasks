You are a web developer building a new log analysis feature to track client session lifecycles for your web application. 

Your task is to build a Python-based parser with a state machine, use it to extract valid sessions, merge the results with a historical dataset, generate a unified diff, and write unit tests for your logic.

**Step 1: State Machine & Parser**
There is a log file located at `/home/user/server.log`. Each line contains space-separated values: `TIMESTAMP USER_ID EVENT`.
The possible events are: `CONNECT`, `AUTH`, `REQUEST`, `DISCONNECT`.
Every user starts in an implicit `OFFLINE` state. 
The valid state transitions for a user are:
- `OFFLINE` -> `CONNECT`
- `CONNECT` -> `AUTH`
- `CONNECT` -> `DISCONNECT`
- `AUTH` -> `REQUEST`
- `REQUEST` -> `REQUEST`
- `REQUEST` -> `DISCONNECT`
- `AUTH` -> `DISCONNECT`
- `DISCONNECT` -> `OFFLINE`

Write a Python script at `/home/user/parser.py` that reads `/home/user/server.log` line by line. It must track the state of each `USER_ID`. 
A user session is considered "Valid" ONLY IF:
1. They follow only valid state transitions.
2. Their final recorded state in the log is `DISCONNECT` (meaning they cleanly finished).
If a user performs an invalid transition (e.g., `REQUEST` while `OFFLINE`, or `CONNECT` while already `CONNECT`), they are immediately marked as "Invalid" and cannot be valid even if they disconnect later.

The script must write the `USER_ID` of all "Valid" users to `/home/user/valid_users.txt`, one per line, sorted alphabetically.

**Step 2: Sorting, Merging, and Diffing**
You have a baseline file of previously seen valid users at `/home/user/historical.txt`.
Using shell commands or Python, combine `/home/user/valid_users.txt` and `/home/user/historical.txt`. Remove duplicates and sort them alphabetically. Save this combined list to `/home/user/all_users.txt`.

Then, use the `diff` command to create a unified diff between `/home/user/historical.txt` and `/home/user/all_users.txt`. Save the output exactly to `/home/user/update.patch`.

**Step 3: Unit Testing**
Write a test file at `/home/user/test_parser.py` that imports your state machine logic and uses `pytest` to test it. You must include at least:
- One test verifying a valid full sequence (`CONNECT` -> `AUTH` -> `REQUEST` -> `DISCONNECT`).
- One test verifying an invalid sequence (e.g., `OFFLINE` -> `REQUEST`).
Ensure you install `pytest` (e.g. `pip install pytest` or `apt-get`) and that running `pytest /home/user/test_parser.py` passes successfully. 

Complete these steps so that `/home/user/valid_users.txt`, `/home/user/all_users.txt`, `/home/user/update.patch`, and `/home/user/test_parser.py` exist and are correct.