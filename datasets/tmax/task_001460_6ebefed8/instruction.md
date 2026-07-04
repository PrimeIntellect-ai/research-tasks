You are assisting a researcher in organizing and preprocessing a video dataset for a machine learning model. The researcher has a raw experiment video located at `/app/experiment_feed.mp4`. 

You need to build a pipeline to process this video and format it correctly.

Please perform the following steps:
1. **Frame Extraction & Processing**: 
   Extract frames from `/app/experiment_feed.mp4` at exactly 4 frames per second (FPS). 
   Convert each extracted frame to grayscale and resize it to exactly 128x128 pixels using bilinear interpolation.

2. **Archive Creation**:
   Pack all the processed frames into a single NumPy compressed archive (`.npz`) located at `/home/user/dataset.npz`. 
   The archive must contain a single array named `frames` with the shape `(N, 128, 128)` and data type `uint8`, where `N` is the total number of extracted frames. The frames should be ordered chronologically.

3. **Data Chunking**:
   Read `/home/user/dataset.npz` and split the `frames` array into smaller sequential chunks of exactly 50 frames each (the last chunk may contain fewer than 50 frames). 
   Save these chunks in the directory `/home/user/chunks/` as `chunk_000.npz`, `chunk_001.npz`, etc., where each file contains a `frames` array.

4. **Directory Watcher (Script only)**:
   The researcher also needs a way to automate this in the future. Write a Python script at `/home/user/watcher.py` that uses the `watchdog` library to monitor the directory `/home/user/incoming/` for any new `.mp4` files. When a new file is detected, it should automatically process it following steps 1 and 2, saving the resulting `.npz` file in `/home/user/processed/` with the same base name as the video. You do not need to run this script, just write it.

Ensure all directories exist and the final `.npz` files are correctly formatted. Your preprocessing will be evaluated against a reference implementation using Mean Squared Error (MSE) to ensure no severe compression artifacts or incorrect interpolations were introduced.