You are a data engineer building an ETL pipeline to process video feeds from traffic cameras. Your goal is to build a high-performance scene-change detection component using dimensionality reduction and similarity search, implemented in Go. 

The pipeline requires extracting features from video frames, projecting them into a lower-dimensional embedding space using a pre-trained linear projection model, and finding frames where the semantic similarity drops below a threshold.

Here are your instructions:

1. **Environment & Feature Extraction:**
   - A video file is located at `/app/data/traffic_cam.mp4`.
   - Use `ffmpeg` to extract exactly one frame per second from the video.
   - For each extracted frame, convert it to grayscale and resize it to exactly 4x4 pixels. Flatten this 4x4 image into a 16-dimensional vector of integers (0-255, reading left-to-right, top-to-bottom).

2. **Model Architecture Reconstruction (Go):**
   - Write a Go program at `/home/user/infer.go` and compile it to `/home/user/bin/infer`.
   - The program must read a JSON array of 16-dimensional float64 arrays from `stdin` (representing a sequence of frames).
   - The program must load model weights from `/app/data/weights.csv` (a 16x8 matrix) and biases from `/app/data/biases.csv` (8 values).
   - Implement the inference step to project the 16D input into an 8D embedding space: `Embedding = ReLU(Input * Weights + Bias)`. (ReLU means replace any negative values with 0). Use `float64` for all math.

3. **Similarity Search & Scene Detection:**
   - For each frame `i` (where `i > 0`), compute the Cosine Similarity between its 8D embedding and the embedding of frame `i-1`.
   - If the norm of either vector is exactly 0, consider their Cosine Similarity to be 1.0.
   - A "scene change" occurs if the Cosine Similarity is strictly less than `0.8000`.
   - The Go program must output to `stdout` a valid JSON array of integer indices representing the frames that triggered a scene change. (e.g., `[2, 5, 12]`). Do not output any other text to `stdout`.

4. **Integration:**
   - After compiling your Go program, use standard Linux CLI tools to pipe the 16D vectors extracted from the video (formatted as a JSON array of arrays) into your `/home/user/bin/infer` program and save the resulting JSON array of scene changes to `/home/user/video_scene_changes.json`.

Ensure your Go implementation is highly accurate, as it will be subjected to rigorous automated fuzz testing against a reference implementation using thousands of random input sequences.