You are a system engineer tasked with fixing a broken backend service, setting up a reverse proxy, and creating a monitoring script. 

Currently, there is a background process script located at `/home/user/watcher.sh` that is supposed to launch a Python web service (`/home/user/backend/app.py`). However, the service keeps crashing immediately upon startup. The service is supposed to listen on port 9090.

Your tasks are as follows:

1. **Diagnose and Fix the Startup Issue**: 
   The `app.py` service crashes because of an issue related to its execution environment in `/home/user/watcher.sh`. Specifically, `app.py` relies on reading a local `config.json` file, but the watcher runs it with the wrong working directory.
   Modify `/home/user/watcher.sh` so that `app.py` runs successfully. Once fixed, execute `/home/user/watcher.sh` in the background so that `app.py` is running and listening on `127.0.0.1:9090`.

2. **Set up a Reverse Proxy**:
   Write a Python script at `/home/user/proxy.py` that acts as a simple reverse proxy. It must:
   - Listen on `127.0.0.1:8080`.
   - Forward all incoming incoming HTTP GET requests to `http://127.0.0.1:9090`.
   - Return the exact HTTP response (status code, headers, and body) received from the backend service to the client.
   - Run this proxy in the background.

3. **Monitor and Extract Data**:
   The backend service exposes an endpoint at `/api/health`. 
   Write a Python script at `/home/user/check.py` that:
   - Makes an HTTP GET request to the reverse proxy at `http://127.0.0.1:8080/api/health`.
   - Parses the returned JSON response.
   - Extracts the value associated with the key `"status"`.
   - Writes this extracted string to a file at `/home/user/result.log`.
   - Execute this script so that `/home/user/result.log` is generated.

Do not remove or alter `app.py` or `config.json`. You must ensure both the backend service and the reverse proxy remain running in the background when your work is complete.