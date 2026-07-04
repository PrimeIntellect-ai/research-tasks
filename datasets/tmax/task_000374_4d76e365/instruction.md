You are an operations engineer tasked with fixing a broken microservice application. 

We have a custom application located in `/app/`. It consists of three Python services that are currently started via a bash script `/app/start_all.sh`. 

The services are:
1. `kv_store.py`: A raw TCP key-value store on `127.0.0.1:8001`. It artificially takes 3 seconds to initialize before binding the port.
2. `backend.py`: An HTTP API on `127.0.0.1:8002`. During startup, it attempts to connect to `127.0.0.1:8001` to verify the KV store is reachable. If it cannot connect, it crashes immediately.
3. `frontend.py`: An HTTP API on `127.0.0.1:8003`. It requires the backend to be available and proxies requests to it.

Currently, if you run `/app/start_all.sh`, the services start simultaneously in the background. Because `kv_store.py` takes time to initialize, `backend.py` crashes, which in turn causes `frontend.py` to fail or return 502s.

Your tasks:
1. Fix the startup sequence. You must modify `/app/start_all.sh` so that it starts `kv_store.py`, waits for it to become healthy (listening on port 8001), then starts `backend.py`, waits for port 8002, and finally starts `frontend.py`. You can use standard bash tools (like `nc`, `sleep`, loops) to implement this health check sequencing.
2. Ensure that running `/app/start_all.sh` leaves all three processes running in the background.
3. Write a Python health check script at `/home/user/health_monitor.py`. This script should:
   - Make an HTTP GET request to `http://127.0.0.1:8003/api/data`.
   - Read the JSON response.
   - Write the exact JSON response text to `/home/user/status.log`.

Do not modify the Python service files in `/app/` directly; only modify `/app/start_all.sh` and create the new `health_monitor.py` script.
Ensure the final state has all three services running on their respective ports.