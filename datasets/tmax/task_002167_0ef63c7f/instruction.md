You are an MLOps engineer tasked with tracking and analyzing experiment artifacts. We have an experiment recording at `/app/experiment_record.mp4`. Your job is to process this video, compute feature embeddings for the frames, perform a correlation analysis to find significant visual shifts (anomalies), and expose your results via an HTTP API.

Please complete the following steps:
1. **Frame Extraction**: Extract the frames from the video at exactly 1 frame per second. Name the frames with a zero-padded 2-digit index starting from 00 (e.g., `frame_00.jpg`, `frame_01.jpg`, etc.).
2. **Embedding Computation**: For each extracted frame:
   - Convert the image to grayscale (use standard luminosity conversion, e.g., Pillow's `Image.convert('L')`).
   - Resize the image to 32x32 pixels using Bilinear interpolation.
   - Flatten the resulting 32x32 matrix into a 1024-dimensional vector of integers (0-255). This is the embedding for the frame.
3. **Correlation Analysis**: Compute the Pearson correlation coefficient between the embeddings of consecutive frames. Frame $t$ is considered an "anomaly" if $t \ge 1$ and the Pearson correlation between frame $t$ and frame $t-1$ is strictly less than 0.85.
4. **Service**: Create and run an HTTP service (using Flask, FastAPI, or similar) listening on `127.0.0.1:8080`.
   It must expose the following endpoints:
   - `GET /anomalies` : Returns a JSON response containing the list of anomaly frame indices (integers). Format: `{"anomalies": [index1, index2, ...]}`.
   - `GET /correlation?f1={t1}&f2={t2}` : Returns the Pearson correlation coefficient between the embedding of frame `t1` and frame `t2`. The response must be JSON in the format: `{"correlation": float_value}`, where `float_value` is rounded to 4 decimal places.

Leave the service running in the background or foreground so that we can query it. You may install any necessary Python packages (like `Pillow`, `numpy`, `scipy`, `fastapi`, `flask`, etc.).