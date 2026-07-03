I am a researcher organizing experimental datasets, and I need your help to build a reproducible data processing pipeline. We have a laboratory recording located at `/app/experiment.mp4`. 

Your task consists of two parts:

Part 1: ETL Pipeline & Feature Extraction
I need you to extract the frame-by-frame average Red, Green, and Blue (RGB) pixel intensities from `/app/experiment.mp4`. Use `ffmpeg` to extract the frames (at 1 frame per second) and compute the average R, G, and B values for each frame. Save the results in a CSV file at `/home/user/video_features.csv` with the headers `frame,R_avg,G_avg,B_avg`.

Part 2: Feature Engineering & Correlation Analysis (C++)
I need a highly accurate, optimized C++ program that computes a rolling covariance matrix of the R, G, and B features over a sliding window. 
Write a C++ program at `/home/user/rolling_cov.cpp` and compile it to `/home/user/rolling_cov`. 
The program must:
1. Read lines from standard input. The first line contains a single integer `W` (the window size, $2 \le W \le 100$).
2. Subsequent lines contain three comma-separated floating-point numbers representing R, G, and B.
3. For each new frame starting from the $W$-th frame, compute the $3 \times 3$ covariance matrix of the features over the last $W$ frames. 
4. Output the 6 unique elements of the covariance matrix (Var(R), Var(G), Var(B), Cov(R,G), Cov(R,B), Cov(G,B)) on a single line, comma-separated, formatted to exactly 6 decimal places.
5. The program should continue processing until EOF.

The numerical accuracy of your C++ program is critical. It must perfectly match my reference implementation's logic. Ensure your sample standard deviation/covariance uses the $(N-1)$ Bessel's correction.

Please write the script, extract the features from the video, and compile the C++ program.