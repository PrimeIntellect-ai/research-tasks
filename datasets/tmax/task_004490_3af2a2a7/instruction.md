You are a performance engineer tasked with debugging and reviving a critical mathematical computation microservice. The service crashed unexpectedly, leaving behind a corrupted database state, a packet capture of the traffic right before the crash, and a screenshot of the original mathematical configuration.

You have the following artifacts in `/app/`:
1. `/app/equation.png` - A screenshot of a whiteboard containing a critical mathematical constant used by the algorithm. It is written in the format `MODULUS=<number>`.
2. `/app/state.db` and `/app/state.db-wal` - An SQLite database containing the service's configuration. The service crashed before writing the latest `AUTH_TOKEN` to the main database file; it is trapped in the Write-Ahead Log (WAL).
3. `/app/requests.pcap` - A packet capture of the HTTP traffic to the service leading up to the crash.
4. `/app/server.py` - The Python source code for the Flask service.

Your objectives:
1. **Extract the Constant:** Analyze `/app/equation.png` to read the `MODULUS` value. Update `/app/server.py` to use this modulus in its `compute_series` function.
2. **Database Recovery:** Recover the uncommitted `AUTH_TOKEN` from the SQLite WAL file. Update the server to require this exact token in the `Authorization: Bearer <token>` header for all POST requests to `/compute`.
3. **Pcap Analysis & Intermittent Failure:** Analyze `/app/requests.pcap` to identify the specific malformed JSON payload that caused the service to crash (it triggers an unhandled mathematical exception or infinite loop). 
4. **Fix the Service:** Patch `/app/server.py` to catch this "poison pill" payload and return an HTTP 400 Bad Request instead of crashing.
5. **Start the Service:** Run the fixed Flask service. It must listen on `127.0.0.1:8888`. 

Ensure the service runs continuously in the background and is ready to accept requests.