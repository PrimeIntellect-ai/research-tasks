We have a local data processing pipeline that relies on a vendored Python package, `datashaper-1.2.0`, located at `/app/datashaper-1.2.0`. There is a systemd user service configured for this package, but it continuously fails to start. 

Your objectives are as follows:

1. **Diagnose and Fix the Service:**
   The service `datashaper.service` (located in `/home/user/.config/systemd/user/`) fails to start. The vendored package has a deliberate configuration issue in its `Makefile` and `worker.py` that silently rejects connections and crashes the service. Find the bug, patch the vendored package, and ensure the systemd user service starts successfully and remains active. 

2. **Network Configuration:**
   The `datashaper` service attempts to listen on port 8080, but the system's firewall (using `iptables` or standard routing) requires local traffic on port 9090 to be forwarded to 8080 for the pipeline to work. Set up the appropriate persistent, idempotent local port forwarding rules so that requests to `localhost:9090` are correctly routed to the service on `localhost:8080`.

3. **Data Transformation Script:**
   The `datashaper` package offloads a specific string transformation task to an external executable. We have a compiled reference implementation at `/app/oracle_transform`. You must write a Python script at `/home/user/transform.py` that replicates the exact behavior of this oracle.
   - The script must read a single string from standard input and print the transformed string to standard output.
   - It must handle ASCII alphanumeric strings of lengths between 1 and 1000 characters.
   - You can test your script's behavior against `/app/oracle_transform` to deduce the transformation logic (e.g., character shifting, reversing, or encoding).

Please complete the fixes, ensure the systemd user service is running, apply the network rules, and write the `/home/user/transform.py` script. The automated test will verify the service state, network routing, and rigorously test your Python script against the oracle using thousands of random inputs.