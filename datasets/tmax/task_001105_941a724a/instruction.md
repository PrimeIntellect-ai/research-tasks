You are an MLOps engineer tasked with analyzing an experiment video artifact and serving similarity metrics. You must build a reproducible data processing pipeline using Bash and C.

Your tasks are as follows:
1. **Frame Extraction**: Write a bash script that uses `ffmpeg` to extract frames from `/app/experiment.mp4`. Extract them at a resolution of 64x64 pixels in raw grayscale format (`gray` pixel format, `.raw` extension). Save them in `/home/user/frames/` named exactly `frame_001.raw`, `frame_002.raw`, etc. (1-indexed).

2. **Dimensionality Reduction**: Write a C program (`/home/user/server.c`) that loads all the extracted raw frames. For each 64x64 frame, reduce its dimensionality to an 8x8 feature matrix (64 dimensions total) by computing the integer average of each 8x8 pixel block. 

3. **Metrics Server**: Your C program must start a TCP server listening on port `9090` on `127.0.0.1`. 
   - When a client connects, it will send a 3-digit frame index followed by a newline (e.g., `015\n`).
   - **Similarity Search**: Find the top 3 most similar frames (excluding the queried frame itself) by calculating the lowest Euclidean distance between their 64-dimensional reduced feature vectors.
   - **Confidence Intervals**: Calculate the global average pixel intensity across *all* original 64x64 frames. Calculate the 95% confidence interval for this global mean using the standard normal distribution (Z = 1.96). Standard error is (sample_std_dev / sqrt(N)). Use population N for std dev calculation.
   - **Response**: The server must reply to the client with exactly this format (and then close the connection):
     `SIMILAR=%03d,%03d,%03d CI=[%.2f,%.2f]\n`
     (where the similar frames are ordered from most similar to least similar, and the CI values are rounded to two decimal places).

4. Compile and run your server in the background so it is ready to receive requests. Save your compilation and startup commands in a reproducible script `/home/user/run_pipeline.sh`.