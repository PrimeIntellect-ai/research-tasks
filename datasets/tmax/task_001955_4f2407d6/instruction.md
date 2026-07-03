You are acting as a log analyst investigating suspicious behavioral patterns. We have a video recording of a dashboard, `/app/movement_log.mp4`, which tracks an entity's movement represented as a single pure white pixel `(RGB: 255, 255, 255)` against a pure black background `(RGB: 0, 0, 0)`. The video is exactly 5 seconds long at 1 FPS (5 frames total).

Your task is to:
1. Extract the (X, Y) coordinates of the white pixel in each of the 5 frames (t=0 to t=4). Top-left is (0,0).
2. Mathematically normalize this reference path. For both the X and Y arrays independently, calculate the Z-score normalized values (subtract the mean, divide by the sample standard deviation with degrees of freedom = 1).
3. Create a Python HTTP web service using `Flask` or `FastAPI` listening on `127.0.0.1:9090`.
4. The service must expose a `POST` endpoint at `/analyze`. 
    - It must accept JSON payloads in the format: `{"auth": "LOG-ANALYSIS-TOK-55", "x_path": [x0, x1, x2, x3, x4], "y_path": [y0, y1, y2, y3, y4]}`.
    - If the "auth" token does not match "LOG-ANALYSIS-TOK-55", return HTTP 401.
    - The endpoint must Z-score normalize the incoming `x_path` and `y_path` using the same logic as above.
    - Calculate the average Euclidean distance between the reference normalized points and the input normalized points (average of the distances at each of the 5 time steps).
    - Constraint-based validation: If the average distance is less than or equal to `0.5`, the pattern is considered normal. Otherwise, it is an anomaly.
    - Return a JSON response: `{"distance": <float_value>, "is_anomaly": <boolean>}`. 

Keep the server running in the background so it can be tested. Write a log file of the extracted raw reference X and Y coordinates to `/home/user/extracted_path.json` in the format `{"x": [...], "y": [...]}`.