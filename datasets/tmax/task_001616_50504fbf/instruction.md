You are a backup administrator tasked with archiving critical footage from a security system. The system provides raw video feeds, but storage constraints require us to archive only specific critical segments with specific visual watermarks, and they must be heavily compressed without dropping below a certain quality threshold.

Your task is to write a C++ program that performs this archiving process. 

Here are the requirements:
1. **Identify the Target Segment**: Search through the directory `/app/backup_metadata/` to find a multi-line log file ending in `.log` that contains a record with `Priority: Critical`. 
   The log records are multi-line and formatted like:
   ```
   [Record Start]
   ID: <number>
   Priority: <level>
   Start_Sec: <number>
   End_Sec: <number>
   [Record End]
   ```
   Parse this file to find the `Start_Sec` and `End_Sec` for the Critical record.

2. **Process the Video**:
   Write a C++ program at `/home/user/archiver.cpp` that uses OpenCV (you may need to install `libopencv-dev` and configure your build). 
   The program must:
   - Open `/app/camera_feed.mp4`.
   - Extract only the video frames between `Start_Sec` and `End_Sec` (inclusive of the start second, up to the end second).
   - Convert the frames to grayscale to save space.
   - Resize the frames to exactly 50% of their original width and height.
   - Write the processed frames to a new video file at `/home/user/archived_segment.mp4` using the 'avc1' (H.264) or 'mp4v' codec.
   
3. **Compression & Quality Threshold**:
   You must tune your VideoWriter parameters (or re-compress the output file using ffmpeg from within your C++ program using `system()`) so that `/home/user/archived_segment.mp4` is heavily compressed.
   - The file size of `/home/user/archived_segment.mp4` MUST be strictly less than 200,000 bytes.
   - The Structural Similarity Index (SSIM) of your processed archive (when scaled back and compared to the grayscale original segment) must be >= 0.85. 
   
Compile and run your C++ program to produce `/home/user/archived_segment.mp4`. Ensure the output file is valid and plays correctly. 

Note: You have full sudo access to install compiler tools, OpenCV, or ffmpeg via `apt-get`.