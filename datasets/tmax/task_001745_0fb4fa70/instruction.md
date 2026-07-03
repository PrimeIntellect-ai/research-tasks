You are a data analyst investigating organizational structure and project allocation for a tech company. 

You have been provided with two CSV files representing a corporate graph:
1. `/home/user/employees.csv` - Contains `emp_id`, `name`, `manager_id`, and `department`.
2. `/home/user/projects.csv` - Contains `emp_id`, `project_name`, and `status`.

Additionally, you have received a recorded audio directive from the Head of Operations located at `/app/audio_directive.wav`.

Your task involves the following phases:
1. **Audio Processing:** Transcribe the audio file `/app/audio_directive.wav` to extract the exact graph processing requirement. You may use standard Linux tools (like whisper or ffmpeg if available) or call out to a local transcription tool you install.
2. **Graph Data Querying (Go):** Write a Go application that loads these CSV files. Using complex recursive logic (e.g., in-memory SQLite with CTEs or custom graph traversal in Go), execute the query requested in the audio directive. The query will involve a hierarchical traversal of the employee graph and an aggregation of their projects.
3. **Service Deployment:** The Go application must not just print the result but serve it via an HTTP REST endpoint. 
   - Listen precisely on `127.0.0.1:8080`.
   - Implement a `GET` endpoint at `/api/v1/projects`.
   - Secure the endpoint. It must only respond to requests including the HTTP header: `Authorization: Bearer GraphMaster2024`.
   - The successful response must be an HTTP 200 OK with a JSON payload in this exact format: `{"result_count": <integer>}`.
   - Any requests missing the token or using an invalid token should return HTTP 401 Unauthorized.

Keep the Go server running in the background once built and executed, so the verification suite can interrogate it.