You are a Machine Learning Engineer preparing training data and building a baseline model to estimate traffic density from a traffic camera video feed.

We have a video file located at `/app/traffic.mp4`. 

Your goal is to complete the following pipeline using **Go**:
1. **Feature Extraction**: Extract frames from `/app/traffic.mp4` using `ffmpeg` at 1 frame per second. For each extracted frame, convert it to grayscale and calculate its statistical variance (pixel intensity variance). This represents a basic "activity" metric.
2. **Correlation Analysis**: Compute the Pearson correlation coefficient between the frame index (time in seconds) and the calculated pixel variance. Output this single float value to `/home/user/correlation.txt`.
3. **Modeling**: Train a simple linear regression model (using any pure Go library or writing it from scratch) that predicts the pixel variance based on the frame index. Perform 5-fold cross-validation to tune or validate your model (print the average Mean Squared Error to `/home/user/mse.txt`).
4. **Inference Benchmarking**: Run a benchmark of 1,000 inference calls on your trained regression model. Save the average inference time (in microseconds) to `/home/user/benchmark.txt`.
5. **Serving**: Create an HTTP server listening on `127.0.0.1:9090`. It must expose an endpoint `GET /predict?frame_id=<int>` which returns a JSON response containing your model's prediction for that frame index. The JSON must exactly match this structure: `{"frame_id": 5, "predicted_variance": 123.45}`. The server must require an Authorization header: `Authorization: Bearer my-secret-token`.

Ensure your Go application is fully compiled and the server is actively running in the background when you finish. Do not exit the terminal or kill the server process. All Go code should be placed in `/home/user/traffic_model/`.