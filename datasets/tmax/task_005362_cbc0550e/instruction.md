My CI build for our `VideoEventService` is completely broken, and I need your help to fix the pipeline, debug the code, and get the service running locally. The codebase is located at `/app/video_service/` (a Git repository).

Here is what you need to do:

1. **Recover the API Secret**: The service requires an authentication token to start up and serve requests. A recent commit mistakenly deleted this token from `config.json`. You need to search the Git repository's history to find the original `AUTH_TOKEN` and restore it to `config.json` under the key `api_secret`.

2. **Database Recovery**: The service relies on an initial configuration database located at `/app/video_service/db/settings.db`. The main database file is currently corrupted, but there is a write-ahead log (`settings.db-wal`) present in the directory. Recover the valid state of the database so that the service can read the `thresholds` table. 

3. **Fix Precision Loss in Video Processing**: The core logic of the service (in `analyzer.py`) processes the test video located at `/app/test_video.mp4`. It scans the video to detect frames where the screen flashes pure red (R > 200, G < 50, B < 50). It then stores the timestamps of these frames. However, the current implementation is suffering from a precision loss bug—it truncates the timestamps to integers, which causes downstream tests to fail. You need to debug and fix `analyzer.py` so that it retains and outputs floating-point timestamps (accurate to at least 3 decimal places).

4. **Start the Service**: Once the code is fixed, the database recovered, and the secret restored, launch the service using the provided `start.sh` script. The service must bind to `127.0.0.1:8080`. 

The automated tests will verify your success by acting as an HTTP client, authenticating with the recovered token, and querying the API for the precise video timestamps. Leave the service running in the background. Write a brief log of the timestamps you found to `/app/video_service/found_timestamps.log` (one float per line).