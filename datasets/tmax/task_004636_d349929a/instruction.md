You are a data scientist working on cleaning a noisy sensor video feed and building an ETL pipeline to detect anomalies.

We have a video feed from a monochromatic sensor located at `/app/noisy_feed.mp4`. Unfortunately, the video suffers from a static background interference pattern. We also have the weights of a pre-trained anomaly detection model saved at `/app/model.pth`.

Your task is to build a reproducible Python pipeline that performs the following steps:
1. **Environment Setup:** Install any necessary Python packages (e.g., `torch`, `opencv-python`, `numpy`, `pandas`).
2. **ETL & Data Cleaning:** 
   - Extract all frames from `/app/noisy_feed.mp4`.
   - Convert the frames to grayscale if they are not already.
   - Clean the data by removing the static background. To do this, compute the median frame across the entire video and subtract this median frame from every individual frame.
3. **Linear Algebra Feature Extraction:** 
   - Flatten each cleaned 2D frame into a 1D vector.
   - Project the flattened vector into a 10-dimensional feature space using a random projection matrix $P$. 
   - To ensure reproducibility, generate $P$ using `numpy` with the following parameters: `np.random.seed(42)` and `P = np.random.randn(frame_width * frame_height, 10)`. Multiply your flattened frame vector (shape `1 x (W*H)`) by $P$ (shape `(W*H) x 10`).
4. **Model Architecture Reconstruction & Inference:**
   - Reconstruct the anomaly detection model using PyTorch. The model is a simple `nn.Sequential` network consisting of:
     - A linear layer taking the 10-dimensional input to 16 hidden units.
     - A ReLU activation.
     - A linear layer projecting the 16 hidden units to 1 output unit.
   - Load the state dictionary from `/app/model.pth` into your reconstructed architecture.
   - Run inference on the 10-dimensional feature vectors for all frames to compute an anomaly score for each frame.
5. **Output:**
   - Save the results to a CSV file at `/home/user/anomaly_scores.csv`.
   - The CSV must contain exactly two columns: `frame_idx` (integer, starting at 0) and `score` (float).

Ensure your pipeline is robust and can be run sequentially to reproduce the CSV.