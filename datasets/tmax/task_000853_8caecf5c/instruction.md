You are a data analyst building an automated bash-based ETL pipeline for video data. We need to extract a 1D "embedding" (file size) from video frames and apply a centering transformation without leaking information from the test set into the train set.

**Step 1: Feature Extraction**
We have a video located at `/app/dashcam.mp4`. 
Using `ffmpeg`, extract the frames of this video at exactly 1 frame per second (fps) as JPEG images.
Create a file named `/home/user/raw_features.csv` containing the "embedding" (file size in bytes) for each frame.
The CSV should have no header and format rows as `frame_num,size`. 
The `frame_num` must be a 4-digit zero-padded number starting from `0001` (e.g., `0001,45210`). Sort the CSV by frame number.

**Step 2: Data Leakage Prevention in Centering**
We want to center our features by subtracting the mean feature value. However, a common mistake (data leakage) is calculating the mean over the entire dataset before splitting into train/test sets.
Write a pure Bash script `/home/user/center_features.sh` that takes two arguments:
1. `<input_csv>` (path to a CSV formatted like `raw_features.csv`)
2. `<N>` (an integer representing the number of frames in the training set)

Your script must:
1. Read the input CSV.
2. Calculate the mean feature size strictly using the first `<N>` rows (the train set). Use standard Bash integer division (floor division).
3. Subtract this training mean from the feature sizes of *all* rows in the dataset (both train and test).
4. Print the result to standard output in the format `frame_num,centered_size`.

Ensure your script `/home/user/center_features.sh` is executable. It must rely only on standard bash built-ins or common coreutils (like `awk`, `sed`, `grep`, `cat`).