You are an MLOps engineer tasked with reconstructing a lost experiment tracking pipeline. We previously used a lightweight feature extractor to generate embeddings from frames of a robotic experiment video (`/app/experiment_record.mp4`). 

The original script (`extract_embeddings.py`) was lost, but we managed to recover the model weights in `/home/user/model_weights.npz`. You need to recreate the script so we can re-compute the embeddings for any given frame index.

Create a Python CLI script at `/home/user/extract_embeddings.py` that takes a single integer argument (the frame index) and prints the resulting embedding.

The pipeline MUST follow these EXACT deterministic steps to be bit-exact with our legacy systems:
1. Open `/app/experiment_record.mp4` using `cv2.VideoCapture`.
2. Extract the specific frame using `cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)` followed by `cap.read()`.
3. Take the BGR image array returned by OpenCV and extract the top-left 32x32 pixel patch (i.e., `patch = frame[0:32, 0:32, :]`).
4. Flatten the patch into a 1D vector of length 3072. (Ensure the order is preserved exactly as flattened by numpy's default C-contiguous flattening).
5. Normalize the vector by dividing all values by `255.0`.
6. Load the weights from `/home/user/model_weights.npz`. The file contains two arrays: `W` (shape 3072 x 16) and `b` (shape 16).
7. Compute the linear projection: `z = (vector dot W) + b`.
8. Apply a ReLU activation: `embedding = max(0, z)` element-wise.
9. Format the resulting 16-dimensional embedding as a comma-separated string, with each value rounded to exactly 4 decimal places (e.g., `0.1234,0.0000,1.5678,...`).
10. Print ONLY this comma-separated string to standard output.

Constraints:
- The script must be written in Python.
- It must handle exceptions gracefully (e.g., if the frame index is out of bounds, print a string of 16 zeros).
- Do not print any debug info or logging to standard output, only the final CSV string.
- You can assume `numpy` and `opencv-python` (`cv2`) are available.