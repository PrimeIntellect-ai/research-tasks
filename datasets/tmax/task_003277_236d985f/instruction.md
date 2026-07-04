As a Machine Learning Engineer, you need to prepare a tool for extracting and matching video frames based on a legacy embedding model. 

We have a video file located at `/app/raw_footage.mp4`. We also have the parameters of a previously trained linear neural network layer saved in `/app/model_params.npz` (contains arrays `W` of shape `(4096, 16)` and `b` of shape `(16,)`).

Your task is to write a Python script `/home/user/find_similar_frame.py` that takes three arguments:
1. The path to an MP4 video file.
2. An integer `N` specifying the number of frames to process (starting from frame 0).
3. A target embedding, provided as a comma-separated string of 16 floating-point numbers.

The script must perform the following steps to find the most similar frame:
1. **Frame Extraction**: Extract the first `N` frames from the input video. To ensure exact pixel-level consistency across platforms, you MUST use `ffmpeg` to extract the frames as raw 64x64 grayscale video. 
   *(Hint: you can use `ffmpeg -i <video> -vframes <N> -f rawvideo -pix_fmt gray -s 64x64 pipe:1` and read `N * 4096` bytes from standard output).*
2. **Feature Engineering**: Convert the raw byte values to floating-point numbers in the range `[0.0, 1.0]` by dividing by 255.0. Flatten each frame into a 4096-dimensional vector.
3. **Model Inference**: Reconstruct the legacy embedding model architecture. Pass the frame vectors through a Linear layer using the weights `W` and bias `b` loaded from `/app/model_params.npz`, followed by a ReLU activation function. This produces a 16-dimensional embedding for each frame.
4. **Similarity Search**: Compute the Cosine Similarity between each frame's embedding and the provided target embedding. (If a frame's embedding is an all-zero vector, its similarity to the target is 0.0).
5. **Recommendation**: Find the frame index (from `0` to `N-1`) that has the highest cosine similarity to the target embedding. In the event of a tie, select the lowest frame index.
6. **Output**: Print the best matching frame index and its cosine similarity score rounded to exactly 4 decimal places, separated by a comma (e.g., `12,0.8543`). Print absolutely nothing else to standard output.

Your script must be robust, self-contained, and output exactly the specified format, as it will be evaluated programmatically against a strict reference implementation using various random target embeddings.