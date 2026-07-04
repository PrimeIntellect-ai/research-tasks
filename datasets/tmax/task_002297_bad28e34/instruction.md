You are a Machine Learning Engineer preparing sequential training data from continuous video feeds. You need to build a lightweight, Bash-only ETL (Extract, Transform, Load) and feature extraction pipeline. 

Your objective is to write a Bash script at `/home/user/pipeline.sh` that takes a single argument (the path to an MP4 video file) and processes it to output a sequence of tokenized features.

The pipeline must perform the following steps sequentially:
1. **Temporal Sampling (Frame Extraction)**: Sample the video at exactly 1 frame per second.
2. **Feature Extraction (Grayscale Brightness)**: For each extracted frame, calculate its average grayscale brightness as an integer from 0 to 255. 
   *(Hint: You can use `ffmpeg` with filters like `fps=1,scale=1:1,format=gray` to reduce each frame to a single pixel, then output it as raw video and read the byte values.)*
3. **Contextual Inference (1D Convolution)**: Model temporal dynamics by applying a 3-frame moving average over the sequence of extracted brightness values. For a frame at index `i`, its smoothed brightness is computed as:
   `smoothed_i = (b_{i-1} + b_i + b_{i+1}) / 3`
   Assume a zero-padding strategy for out-of-bounds indices (i.e., if `i-1` or `i+1` does not exist, use `0` for that missing value). Do not round the result.
4. **Tokenization**: Map the continuous smoothed brightness values into categorical tokens for training:
   - Strictly less than 85.0: `LOW`
   - 85.0 to 170.0 (inclusive): `MID`
   - Strictly greater than 170.0: `HIGH`

**Output Format**: 
Your script must print the resulting tokens to standard output, exactly one token per line, in chronological order.

For your convenience and iterative testing, a sample video has been provided at `/app/raw_data.mp4`. Ensure your script uses strictly standard Bash tools, coreutils (like `awk`, `tr`, `od`), and `ffmpeg`.