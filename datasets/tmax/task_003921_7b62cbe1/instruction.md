You are an AI assistant helping a machine learning researcher organize a complex video dataset. The researcher has a continuous video recording of an experiment and a messy collection of nested metadata files. You need to extract specific frames, match them with their scattered metadata, standardize the structure, and prepare a backup archive.

Here is the current system state:
1. A video file of the experiment is located at `/app/experiment.mp4`.
2. A directory at `/home/user/raw_metadata/` contains nested folders with thousands of poorly named JSON files. Each valid JSON file contains a key `"target_frame"` indicating the video frame it describes.

Your task is to write and execute Python scripts or shell commands to perform the following:

**Step 1: Frame Extraction**
Process the video file `/app/experiment.mp4`. Extract exactly every 25th frame from the video (i.e., frame index 0, 25, 50, 75, etc.). Save these images temporarily as JPEG files. 

**Step 2: Recursive Metadata Traversal & Matching**
Recursively traverse `/home/user/raw_metadata/` to find all `.json` files. Parse them to read the `"target_frame"` value. Match each extracted frame from Step 1 with its corresponding JSON metadata file.

**Step 3: Bulk Renaming and Hard Link Management**
Create a unified dataset directory at `/home/user/curated_dataset/`. For every matched frame and metadata pair, create a **hard link** to both the image and the JSON file inside `/home/user/curated_dataset/`. During this process, standardize the file names to exactly match this pattern:
`sample_XXXXXX.jpg` and `sample_XXXXXX.json`
Where `XXXXXX` is the frame index padded to exactly 6 digits (e.g., `sample_000025.jpg`).

**Step 4: Incremental Backup**
Write a Python script that creates a compressed archive named `/home/user/dataset_backup.tar.gz` containing the contents of `/home/user/curated_dataset/`. Ensure that the archive process does not dereference the hard links (it should preserve them as hard links within the archive to save space).

*Note: You may need to install libraries like `opencv-python` or use system tools like `ffmpeg` to handle the video processing.*