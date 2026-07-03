Hello, IT Support! We have a critical ticket escalated to our queue regarding the new Sensor Aggregation Pipeline.

Users are reporting two main issues:
1. The aggregation service occasionally returns `NaN` for sensor averages when under heavy load, causing downstream financial models to fail. This is an intermittent failure.
2. The service crashes entirely when legacy sensors send corrupted or malformed JSON payloads.

The system is located in `/home/user/app/` and consists of three components:
- A Go-based `collector` service that receives HTTP POST requests with sensor data and computes a running exponential moving average.
- A local Redis instance used to store the latest averages.
- A Go-based `api` service that serves the aggregated data to clients.

Currently, the startup script `/home/user/app/start.sh` is failing because the services aren't configured to talk to each other correctly, and the Go code has severe bugs.

Your tasks are:
1. **Comprehend and Fix the Go Code**: Debug `/home/user/app/collector/main.go`. Fix the concurrency issue causing numerical instability (NaNs) during simultaneous updates. Implement robust error handling so that corrupted JSON payloads are ignored (returning HTTP 400) rather than panicking the server.
2. **Configure the Services**: Edit `/home/user/app/config.env` so the `collector` and `api` services correctly connect to the local Redis instance (which runs on port 6379).
3. **Bring up the Pipeline**: Ensure the `collector` listens on HTTP port `8081` and the `api` service listens on HTTP port `8082`.
4. **Authentication**: The `api` service expects an Authorization header for reads. Ensure your configuration sets the `API_TOKEN=secret-token-99` in the environment so legitimate clients can authenticate.

Once fixed, execute `/home/user/app/start.sh` to leave all services running in the background. Automated tests will verify the fix by sending a mix of concurrent valid requests, malformed requests, and authenticated read requests.