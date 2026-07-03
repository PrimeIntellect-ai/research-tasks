You are an operations engineer debugging a failing log processing pipeline.

The pipeline consists of a Node.js API Gateway and a Python Flask backend. You can find the source code and configuration for these services in `/home/user/app/`. 
To bring up the services, you can run the startup script: `bash /home/user/app/start.sh`.

Recently, the log processor has been hanging and timing out when processing certain batches of logs. 

Your tasks:
1. **Container Debugging & Delta Debugging**: A recent log batch that caused the system to hang is located at `/home/user/app/data/massive_log.txt`. It contains 5,000 log lines. Use delta debugging / bisection to identify the **single line** that triggers an infinite loop or recursion error in the backend. Save this exact single log line to `/home/user/isolated_bug.txt`.
2. **Loop / Recursion Fixing**: Inspect the log parsing logic in the Python backend at `/home/user/app/backend/parser.py`. Identify why the toxic log line causes an infinite loop. Fix the code so that if it encounters this malformed pattern, it safely returns the string `"malformed"` instead of hanging.
3. **Bring the system up**: Ensure the fixed backend and the Node.js API gateway are running. The API gateway must listen on `localhost:5000` and successfully handle HTTP POST requests to `/process_logs` without hanging, even when the malicious log line is present in the payload.

Leave the services running in the background once fixed so the verification system can test them.