You are an IT support technician responding to an escalated internal ticket. 

A user has reported that our Python API backend crashes intermittently when they try to pull historical records using a specific combination of filters. The user attached a screenshot of their console when the error occurred, which we have saved at `/app/ticket_screenshot.png`. 

The original complex filter payload that causes the crash has been saved to `/home/user/ticket_payload.json`.

Your tasks:
1. Extract the `API Token` and the `User ID` from the screenshot at `/app/ticket_screenshot.png` (you may use `tesseract` or another OCR tool).
2. The buggy server code is located at `/home/user/api_server.py`. It reads an SQLite database at `/home/user/records.db`. 
3. Use delta debugging/minimization principles to determine exactly which combination of parameters in `/home/user/ticket_payload.json` causes the SQL query generation to fail or return erroneous results. The bug is known to be an intermittent query result error depending on the presence of certain filter flags.
4. Fix the bug in `/home/user/api_server.py` so that it correctly handles all parameters without crashing or throwing a 500 error.
5. Once fixed, start the API server so that it listens on `127.0.0.1:8080`. 

The server must run continuously in the background or in a separate terminal session. The automated verification system will send HTTP GET requests to `http://127.0.0.1:8080/api/v1/records/<User ID>?token=<API Token>` using various subsets of the original payload to ensure the bug is resolved and no 500 errors are returned.