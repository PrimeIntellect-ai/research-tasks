We are porting an old shell-based video analysis tool into a minimal containerized web service. You need to write a Python HTTP web server that processes a provided video file and logs the results. 

The video file is located at `/app/video.mp4`.

Your task is to create and start a Python web server (e.g., using Flask or FastAPI) listening on `127.0.0.1:8080`. Leave the server running in the background so it can be tested.

The server must meet the following requirements:

1. **Schema Migration:** On startup, the server must initialize a SQLite database at `/app/metrics.db`. It should execute a schema migration to create a table named `metrics` with the following columns: `id` (INTEGER PRIMARY KEY), `frame` (INTEGER), and `brightness` (REAL).
2. **Endpoint:** Expose a `POST /analyze` endpoint that accepts a JSON payload in the format: `{"frame": <int>}`.
3. **Request Validation:** If the `frame` key is missing, is not an integer, or is less than 0, return an HTTP 400 Bad Request response.
4. **Rate Limiting:** Implement a simple global rate limit of **5 successful requests per minute**. If a client makes a 6th valid request within a minute, the server must reject it with an HTTP 429 Too Many Requests response. (Invalid requests that return 400 do not count towards the rate limit).
5. **Numerical Algorithm (Video Processing):** For a valid request, extract the exact 0-indexed frame number from `/app/video.mp4`. Convert the frame to grayscale and calculate the average pixel brightness (a float representing the mean of all pixel intensities in that frame). You may use OpenCV (`cv2`) for this.
6. **Persistence:** Insert the `frame` number and calculated `brightness` into the `metrics` table.
7. **Response:** Return an HTTP 200 OK response with a JSON payload in the format: `{"brightness": <float>}`.

Ensure your server is running and bound to `127.0.0.1:8080` before finishing your turn. You may install any necessary Python packages (like `flask` and `opencv-python-headless`) via pip.