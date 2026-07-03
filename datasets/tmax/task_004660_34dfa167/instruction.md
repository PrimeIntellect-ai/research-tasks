You are tasked with building a specialized Rust microservice to expose an optimized audit query for our security telemetry database.

We have a SQLite database located at `/app/logs.db`. It contains two tables:
1. `users` (columns: `id` INTEGER, `email` TEXT, `metadata` TEXT) 
   - `metadata` is a JSON string containing various fields, including a `department` key.
2. `logins` (columns: `id` INTEGER, `user_id` INTEGER, `status` TEXT, `timestamp` DATETIME)
   - `status` can be 'SUCCESS' or 'FAILED'.

Your goals are:
1. **Decode the Audio Specification**: Listen to the audio file located at `/app/specs.wav`. This voice memo from our lead security engineer dictates three critical configuration values for your service:
   - The exact port number the server should listen on (localhost).
   - The URL endpoint path for the query.
   - The exact Bearer token required to authorize requests to this endpoint.

2. **Develop the Rust Service**: Create a new Rust project at `/home/user/audit_service`. Write an HTTP web server (e.g., using `axum` or `actix-web`) that listens on the designated port and endpoint.
   - The endpoint must strictly require the Bearer token specified in the audio file. Unauthenticated requests should be rejected with a 401 Unauthorized status.
   
3. **Optimize & Execute the Query**: When the endpoint is hit, it must execute a highly efficient SQL query against `/app/logs.db` to find all users in the 'Engineering' department (extracted from the `metadata` JSON) who have had strictly **more than 3** 'FAILED' login attempts.
   - The endpoint must return a JSON response containing an array of objects matching this exact schema:
     `[ { "user_id": <int>, "email": "<string>", "failed_attempts": <int> }, ... ]`
   - The results must be ordered by `failed_attempts` descending, then by `user_id` ascending.

Make sure your Rust service is compiled and actively running in the background when you complete your task, so our automated integration tests can query the endpoint. You may use any standard community crates (e.g., `rusqlite`, `serde`, `serde_json`, `tokio`, `axum`).