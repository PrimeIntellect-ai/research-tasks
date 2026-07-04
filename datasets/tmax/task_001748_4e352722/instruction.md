You are a performance engineer tasked with resolving a critical issue in our data processing service. 

Our internal HTTP API, vendored at `/app/fast-csv-api` as a Git repository, has suddenly started experiencing complete hangs when processing certain data streams. We suspect a recent commit introduced a severe performance regression or infinite loop when handling corrupted inputs.

We have captured a payload that triggers the hang, located at `/home/user/bad_input.csv`.

Your objectives:
1. **Delta Debugging / Minimization:** Analyze `/home/user/bad_input.csv` to isolate the exact single line of CSV that causes the processor to hang. Save this single line exactly as it appears (no trailing newline required) into `/home/user/poison_pill.txt`.
2. **Regression Finding:** Use Git history within `/app/fast-csv-api` to understand the root cause.
3. **Fix the Code:** Patch the Python code in `/app/fast-csv-api` to handle the corrupted input gracefully without hanging (it should either skip the corrupted field or return an error, but it must not hang).
4. **Deploy:** Start the API server to listen on `127.0.0.1:8080` by running `python server.py` from within the `/app/fast-csv-api` directory. Leave it running in the background.

The automated verification will:
- Check the contents of `/home/user/poison_pill.txt`.
- Send an HTTP POST request containing the poison pill payload to `http://127.0.0.1:8080/process`. It expects the server to respond with an HTTP 200 within 1 second, confirming the hang has been resolved.

Do not change the server's port or endpoint path. Use Python and standard Linux utilities.