You are tasked with building a data cleaning pipeline for a large dashboard camera dataset. Some of the video frames have been corrupted by sensor glitches, which manifest as a small, pure red 10x10 artifact (RGB: 255, 0, 0) somewhere in the image.

We need you to extract the data, build a reliable detector to filter out corrupted frames, and package the cleaned data efficiently for downstream machine learning tasks.

Here are the requirements:

1. **Frame Extraction**: Extract frames from the video file located at `/app/dashcam_raw.mp4` at exactly 1 frame per second (1 fps). 

2. **Detector Development**: We have provided a small set of training examples in `/app/corpora/train/clean/` and `/app/corpora/train/evil/`. You must write a standalone classifier script located at `/home/user/detector.py`. 
   - The script must accept a single command-line argument: the absolute path to an image file.
   - The script must evaluate the image and print exactly `CLEAN` or `EVIL` to standard output (and nothing else).
   - *Note*: An automated test suite will rigorously verify this script against a separate, hidden set of clean and evil images.

3. **Video Frame Filtering**: Apply your detection logic to the frames you extracted from `/app/dashcam_raw.mp4`. 
   - Identify all the cleanly extracted frames (those without the sensor glitch).
   - Write the 0-indexed frame numbers of these CLEAN frames to a text file at `/home/user/video_clean_frames.txt`. Each frame number should be on a new line, sorted in ascending order.

4. **Large-Scale Data Storage**: Storing thousands of individual image files is inefficient for training. To package the cleaned data, create an HDF5 file at `/home/user/clean_dataset.h5`. 
   - Inside the HDF5 file, create a single dataset named `images` containing the uncompressed image data of all the CLEAN frames from the video, in the exact chronological order they appeared.
   - The dataset must have the shape `(N, H, W, 3)`, where `N` is the number of clean frames, and `H` and `W` are the dimensions of the frames. The data type must be `uint8`, representing the RGB channels.

Ensure your `detector.py` is robust and your final HDF5 file matches the specifications perfectly.