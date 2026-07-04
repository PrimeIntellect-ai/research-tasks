You are an MLOps engineer tasked with building a reproducible artifact-tracking pipeline for an audio processing experiment. Your goal is to chunk a long continuous audio recording, extract basic acoustic features, compute the correlation between these chunks, and perform a basic similarity recommendation.

You must create a reproducible pipeline script `/home/user/run_pipeline.sh` that orchestrates this entire process. You may use standard Linux command-line tools (like `ffmpeg`) and Python 3.

**Pipeline Specifications:**
Your script `/home/user/run_pipeline.sh` must take exactly two arguments:
1. Input audio file path (e.g., `/app/experiment_audio.wav`)
2. Output artifacts directory (e.g., `/home/user/artifacts`)

When executed as `bash /home/user/run_pipeline.sh <input_audio> <output_dir>`, your script must perform the following deterministic steps:

1. **Storage Management & Chunking**: 
   - Ensure the `<output_dir>` exists (create it if not, and clear its contents if it does).
   - Create a `<output_dir>/chunks` subdirectory.
   - Using `ffmpeg`, split the input audio into exact **1-second** non-overlapping segments. Name them `chunk_00.wav`, `chunk_01.wav`, ..., `chunk_NN.wav`. 
   - *Assume the input audio's duration in seconds is exactly an integer.*

2. **Feature Extraction**:
   - Write a Python script (called by your bash script) that processes each chunk.
   - For each 1-second chunk, assuming a 16,000 Hz sample rate, you will have 16,000 samples.
   - Split these 16,000 samples into exactly **10 sequential windows** of 1,600 samples each.
   - For each window, compute the **Mean Absolute Value (MAV)** of the audio samples. 
   - This results in a 10-dimensional feature vector $[F_0, F_1, ..., F_9]$ for each chunk.

3. **Correlation & Covariance Analysis**:
   - Using the feature vectors for all $N$ chunks (ordered `chunk_00` to `chunk_{N-1}`), compute the $N \times N$ Pearson correlation matrix.
   - Save this matrix to `<output_dir>/correlation.csv`. It must be a comma-separated text file with no header row and no index column. Format all numbers to 6 decimal places.

4. **Similarity Recommendation**:
   - Using the computed correlation matrix, identify the **top 3** chunks that are most similar (highest Pearson correlation) to `chunk_00.wav`, excluding `chunk_00.wav` itself.
   - Write the integer indices of these 3 chunks to `<output_dir>/similar.txt`, separated by commas (e.g., `5,12,3`). Sort them in descending order of correlation. (If there is a tie, sort by chunk index ascending).

**Execution:**
Once you have written your code, execute your pipeline using the provided audio fixture:
`bash /home/user/run_pipeline.sh /app/experiment_audio.wav /home/user/artifacts`

Ensure that the files `/home/user/artifacts/correlation.csv` and `/home/user/artifacts/similar.txt` are successfully generated and strictly follow the formatting requirements.