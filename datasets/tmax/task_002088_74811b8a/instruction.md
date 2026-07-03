You are a data analyst working on a multi-modal sensor fusion project. You have been given a video recording and two separate CSV files containing sensor readings. Your goal is to extract visual features, join them with the sensor data, perform dimensionality reduction using C++, test the numerical accuracy of your reduction, and finally serve the results via an HTTP API.

Here are your steps:

1. **Feature Extraction**: 
   A video file is located at `/app/data/experiment.mp4`. Extract the mean Red, Green, and Blue (RGB) pixel values for each frame (0-indexed).
   
2. **Multi-source Data Joining**:
   Join your extracted RGB features with two sensor data files: `/app/data/sensor_a.csv` and `/app/data/sensor_b.csv`. Both CSVs contain a `frame_id` column. Merge them so that each `frame_id` has exactly 23 features: `R, G, B` followed by the 10 features from `sensor_a` and 10 features from `sensor_b`. Sort the features such that R, G, B are first, then `sensor_a` features in their original order, then `sensor_b` features in their original order.

3. **Dimensionality Reduction & Numerical Accuracy (C++)**:
   Write a C++ program (e.g., `pca_processor.cpp`) that reads the joined dataset. 
   - Standardize the 23 features (subtract mean, divide by standard deviation for each feature).
   - Perform Principal Component Analysis (PCA) to reduce the 23-dimensional data to exactly 2 principal components (PC1 and PC2). You may use the Eigen library (e.g., `apt-get install libeigen-dev`).
   - Calculate the reconstruction error for each frame (the Mean Squared Error between the standardized 23-dimensional original features and the features reconstructed from just PC1 and PC2).
   - Output the results (frame_id, pc1, pc2, reconstruction_error) to a file or keep it in memory for the next step.

4. **Serving via HTTP**:
   Start an HTTP server listening on `0.0.0.0:9090`. You can write the server in C++ (e.g., using `cpp-httplib`) or write a lightweight Python wrapper that reads your C++ output and serves it.
   The server must expose the following endpoint:
   - `GET /api/pca/<frame_id>`
   It should return an `application/json` response with the exact format:
   `{"frame_id": <int>, "pc1": <float>, "pc2": <float>, "reconstruction_error": <float>}`
   
Ensure your HTTP server remains running in the background or foreground so that our automated test suite can query `http://127.0.0.1:9090/api/pca/<frame_id>` to verify your results. All missing dependencies (like ffmpeg, eigen, python libraries) must be installed by you.