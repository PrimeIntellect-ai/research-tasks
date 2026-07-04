You have inherited a broken, undocumented microservice system consisting of a Python ingestion worker and a Node.js API server. The system is currently non-functional due to dependency conflicts, parsing crashes, and missing configuration.

Your objectives are to debug and restore the system, then bring up the Node.js service so it can be verified.

1. **Configuration Recovery**:
   The original configuration file was lost, but a screenshot of it remains at `/app/config_snapshot.png`. Use OCR (e.g., `tesseract`) to read this image. It contains the environment variables `API_PORT` and `API_KEY`. You will need these to run the Node.js service.

2. **Log Timeline Reconstruction**:
   The system previously crashed while processing a specific transaction: `TXN-8842`. 
   Examine the logs in `/app/logs/ingest.log` and `/app/logs/api.log`. Find the exact ISO8601 timestamp of the *first* error message related to `TXN-8842` across both services. Write this exact timestamp (e.g., `2023-10-01T12:00:00Z`) to a file named `/app/crash_time.txt`.

3. **Dependency and Parsing Fixes**:
   - The Python script `/app/ingest.py` currently fails to run because of a dependency conflict in `/app/requirements.txt`. Fix the `requirements.txt` so that all packages install successfully without pip errors.
   - Once running, `/app/ingest.py` crashes due to a format parsing edge case when reading historical data (specifically when the `payload.user_id` field is missing or null). Modify `/app/ingest.py` so that it catches this edge case, logs a warning, and continues processing instead of throwing an exception.

4. **Service Bring-up**:
   - Start the Node.js service located at `/app/api.js`. You must start it such that it listens on the port specified by `API_PORT` from the image, and requires the `X-API-KEY` header matching the `API_KEY` from the image for all requests. (You can pass these as environment variables `PORT` and `SECRET_KEY` when running `node /app/api.js`).
   - Leave the Node.js API running in the background. It must successfully respond to HTTP GET requests on `/health`.

Ensure the Node.js server is actively listening on the correct port before you finish.