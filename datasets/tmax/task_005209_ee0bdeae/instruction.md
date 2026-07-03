You are an SRE troubleshooting a legacy monitoring system. Our datacenter has a physical status dashboard, and a webcam captures its state continuously. Due to a recent environment misconfiguration, our automated script that computes the "Uptime Stability Score" from the dashboard's flashing LEDs has started failing and occasionally producing wild, incorrect floating-point results. 

A snippet of the captured video is available at `/app/dashboard_cam.mp4`. 

First, you need to extract the average grayscale brightness of each frame in the video. 
Second, you need to write a C++ program (`/home/user/stability_calc.cpp`) that reads a sequence of these floating-point brightness values from standard input (one per line) and computes the running variance of the brightness using a numerically stable algorithm (e.g., Welford's online algorithm), since the naive formula previously used suffered from catastrophic cancellation. 

Your C++ program must:
1. Include `assert()` statements to validate that no brightness value is negative and that the variance never drops below zero (assertion-based intermediate validation).
2. Take standard input containing `N` floating-point numbers.
3. Output a single floating-point number representing the final sample variance of the sequence, printed to 6 decimal places.
4. Be compiled to `/home/user/stability_calc`.

Note: The legacy environment is missing standard library linkers in its default `LD_LIBRARY_PATH`. You may need to fix your local environment variables or pass explicit compiler flags to build the C++ code successfully. 

Once you have written and compiled the numerically stable C++ program, extract the frame brightnesses from `/app/dashboard_cam.mp4` using `ffmpeg` and process them through your program, saving the final output to `/home/user/final_variance.txt`.