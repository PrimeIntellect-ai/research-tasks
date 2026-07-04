You are an ML Engineer preparing training data and building an exploratory analysis pipeline for a smart city monitoring project.

You have been provided with:
1. A video artifact at `/app/traffic.mp4`.
2. A tabular sensor log dataset at `/app/sensor_logs.csv`.
3. PyTorch model weights at `/app/embedding_model.pth`.
4. A buggy plotting script at `/app/plot_correlations.py`.

Your pipeline must accomplish the following steps:

**1. Frame Extraction and Model Inference**
Extract frames from `/app/traffic.mp4` at exactly 1 frame per second (fps). 
Reconstruct the PyTorch model architecture to load `/app/embedding_model.pth`. The model is a simple image encoder:
- Input: `(3, 64, 64)` normalized image tensor.
- Conv2d(3, 16, kernel_size=3, stride=2, padding=1), ReLU
- Conv2d(16, 32, kernel_size=3, stride=2, padding=1), ReLU
- Flatten
- Linear(32 * 16 * 16, 16), ReLU
- Linear(16, 4)
Run inference on all extracted, resized (64x64) frames to extract 4-dimensional embeddings.

**2. Data Joining and Correlation Analysis**
Extract the timestamp (in integer seconds, 0-indexed) of each frame. Join the frame embeddings with the corresponding row in `/app/sensor_logs.csv` by matching the frame timestamp (in seconds) to the `time_sec` column. Calculate the Pearson correlation matrix between the 4 embedding dimensions and the 3 sensor features (`temperature`, `humidity`, `luminosity`). 

**3. Fix Plotting Script**
Use the provided `/app/plot_correlations.py` script to generate a heatmap of this correlation matrix. The script runs without errors but currently outputs completely blank plots because the server environment is headless and the matplotlib backend is misconfigured. Fix the script so it correctly renders and saves the plot to `/app/output/correlation_heatmap.png`.

**4. Similarity Search and Service (Multi-Protocol)**
Implement a nearest-neighbor similarity search (using cosine similarity) over the extracted frame embeddings.
Bring up an HTTP API (e.g., using Flask or FastAPI) listening on `0.0.0.0:8000` with the following endpoints:
- `GET /health` -> Returns `{"status": "ok"}`
- `GET /similar?time_sec=<int>` -> Returns the integer timestamps of the top 3 most similar frames (excluding the queried frame itself) as a JSON list: `{"similar_frames": [sec1, sec2, sec3]}`
- `GET /plot` -> Serves the fixed correlation heatmap image (`image/png`).
- `GET /data?time_sec=<int>` -> Returns the joined row data (embeddings + sensor data) for that timestamp: `{"embedding": [e1,e2,e3,e4], "temperature": float, "humidity": float, "luminosity": float}`

Start your service in the background and ensure it remains running.