You are a data scientist tasked with debugging a data pipeline and analyzing a video dataset. We have a traffic monitoring video located at `/app/traffic.mp4`. 

A previous team member wrote a pipeline to extract frame brightness (mean pixel value) and compute its correlation with the frame index to test if the lighting changes significantly over time (hypothesis testing). However, their pipeline silently introduced NaNs during data merging, converting integers to floats and ruining the reproducibility of the statistics.

Your task:
1. Extract frames from `/app/traffic.mp4` at 1 fps using `ffmpeg`.
2. Compute the mean grayscale brightness for each extracted frame.
3. Clean the resulting dataset to ensure no NaNs are present and frame indices remain integers.
4. Compute the Pearson correlation coefficient between the frame index (starting at 1) and the mean brightness.
5. Perform a hypothesis test (t-test) to determine if the correlation is significantly different from 0.
6. Serve the results via an HTTP API. You must bring up a web server listening on `127.0.0.1:8080`.
   - When a `GET /stats` request is made, the server must return a JSON response with the exact format:
     `{"correlation": <float>, "p_value": <float>, "reproducible": true}`
   - The server must handle standard HTTP GET requests and stay running.

Ensure your pipeline is reproducible and the server is actively listening on port 8080.