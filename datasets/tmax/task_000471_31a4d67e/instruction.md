You are an operations engineer triaging an urgent incident. The internal data aggregation service, `data-aggregator`, has been failing to deploy. Furthermore, engineers reported that the previous deployment would frequently freeze and time out under high concurrent load.

The source code for the service has been provided to you in `/app/data_aggregator-1.0.0/`. It is a Python package that provides an HTTP API.

Your objectives are to fix the deployment, resolve the concurrency issue, and start the service:

1. **Fix the Build and Dependencies**: 
   Navigate to `/app/data_aggregator-1.0.0/`. You will find that running `pip install .` fails. Diagnose the build failure and resolve the dependency conflict in the package's configuration. Ensure the package successfully installs in your environment.

2. **Diagnose and Fix the Deadlock**:
   The service uses a multithreaded HTTP server. Look at `data_aggregator/server.py`. The `/process` endpoint deadlocks when handling requests concurrently. Identify the root cause of this concurrency bug and fix the code so it safely handles concurrent requests without freezing.

3. **Add Assertion-Based Validation**:
   In `data_aggregator/server.py`, locate the `process_payload(payload)` function. Before any processing occurs, add a strict Python `assert` statement to validate that the `payload` parameter is a dictionary (`dict`). If it is not, the assertion should fail.

4. **Start the Service**:
   Once fixed and installed, start the server. It must listen on `127.0.0.1:8080`.
   The service requires an API key for access. You must run the server with the environment variable `AGGREGATOR_API_KEY=secret-ops-token`.
   
   To start the server, use:
   `python -m data_aggregator.server`
   
Leave the server running in the background or in an active terminal session so that the automated integration tests can verify the `/process` endpoint. The tests will send concurrent POST requests to ensure the deadlock is resolved.