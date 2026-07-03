You are an observability engineer tuning some dashboard metric extraction tools. We have a VNC recording of a legacy dashboard in a video file located at `/app/dashboard_vnc.mp4`. The video is in 1920x1080 resolution. 

We need to extract the "System Alert" indicator's status over time, which is located exactly in the top-left corner of the dashboard (a 100x100 pixel square: X from 0 to 99, Y from 0 to 99).

Your task is to write a C++ program that takes a single integer command-line argument representing a timestamp in seconds (e.g., `5`), extracts the exact video frame at that timestamp, and calculates the average Red channel intensity (0-255) for the pixels in that 100x100 top-left bounding box.

Requirements:
1. Write your C++ source code to `/home/user/extractor.cpp`.
2. Compile it to an executable at `/home/user/extractor`.
3. The executable must accept a single integer argument `T` (time in seconds).
4. You may use standard CLI tools like `ffmpeg` (e.g., via `popen` or `system()`) to extract the frame data at time `T`. (Hint: You can extract raw RGB24 data for easy parsing in C++).
5. The program should print only the average Red channel value of the 100x100 region, formatted as a floating-point number rounded to exactly 2 decimal places (e.g., `124.50`).
6. Do not print any other text, warnings, or logs to standard output.

You have standard tools installed, including `ffmpeg` and `g++`.