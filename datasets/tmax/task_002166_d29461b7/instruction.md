You are a data analyst analyzing camera footage. A video file is located at `/app/traffic_camera.mp4`.

Your task is to extract analytics from this video and serve them via a local web service.

Please perform the following steps:
1. Extract the frames of the video at exactly 1 frame per second (1 fps).
2. For each extracted frame, calculate a simple 3-dimensional "embedding": the average pixel intensity (0-255) of the Red, Green, and Blue channels, respectively.
3. Compute the 3x3 covariance matrix of these (R, G, B) embeddings across all extracted frames.
4. Calculate a 95% confidence interval for the mean of the Red channel embeddings using the bootstrap method. Use exactly 10,000 bootstrap samples (sampling with replacement) and use the percentile method. Set your random seed to `42` before generating the bootstrap samples to ensure deterministic results.
5. Bring up an HTTP web server listening on `127.0.0.1:8080` that exposes the following endpoints:
   - `GET /covariance`: Returns the 3x3 covariance matrix as a CSV formatted string (no header). Values must be rounded to 4 decimal places.
   - `GET /bootstrap_red`: Returns the 95% confidence interval of the Red channel mean as a CSV formatted string containing a single row with two columns: `lower_bound,upper_bound` (no header, rounded to 4 decimal places).

Use any tools or programming languages you prefer. Ensure your server is running in the background or foreground such that it can accept requests on port 8080.