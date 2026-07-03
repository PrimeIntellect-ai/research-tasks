I have a video of a 4x4 grid of diagnostic LED sensors from a lab experiment at `/app/sensor_feed.mp4`. Each LED blinks to transmit a specific sequence of integer values over time. Unfortunately, the video capture was lossy: some frames are completely blacked out (corrupted), and there is slight compression artifacting. 

Your objective is to build an ETL pipeline in C++ to extract, clean, and decode these signals. 

Here are the specific requirements:
1. **Frame Extraction**: Extract the frames from the video. The video is exactly 10 seconds long at 10 fps (100 frames total).
2. **Feature Extraction (C++)**: Write a C++ program, `extract_signals.cpp`, that reads each frame and calculates the average grayscale intensity of each of the 16 LEDs. The LEDs are arranged in a perfect 4x4 grid. The video resolution is 400x400. Each LED occupies a 100x100 pixel block. 
3. **Data Cleaning & Imputation**: The sensor values are meant to represent integer states (from 0 to 255). Some frames are entirely black (intensity = 0 for all LEDs) due to capture glitches. You must treat these as missing values. Impute these missing values using forward-fill (carry over the last known valid state for that LED). 
    *Warning*: Beware of silent type coercion. Your internal pipeline must handle these imputed values strictly as integers. Do not allow intermediate float conversions during the imputation or aggregation steps, as this mimics a common data science bug where NaNs silently promote arrays to floats, causing precision loss in downstream modular arithmetic.
4. **Tokenization & Mathematical Filtering**: Once the 100x16 matrix of integers is cleaned, apply a discrete convolution over time for each LED using the kernel `[1, -2, 1]`. For the edges (frame 0 and frame 99), pad with the edge value.
5. **Output**: Save the final mathematically filtered 100x16 matrix as a CSV file at `/home/user/filtered_signals.csv`. Each row should correspond to a frame (0 to 99), and each column to an LED (0 to 15, reading left-to-right, top-to-bottom). Ensure the values are comma-separated integers.

Use standard CLI tools (like `ffmpeg`, `imagemagick`) for extraction, and standard C++17 (compiled with `g++`) for the core processing.