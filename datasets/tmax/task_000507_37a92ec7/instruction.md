You are a log analyst investigating a set of corrupted system metric logs. 
You have been provided with two files in the `/app/` directory:
1. `/app/analyst_instructions.wav` - An intercepted audio memo from the lead engineer containing critical parameters for your analysis.
2. `/app/system_metrics.bin` - A raw data file containing wide-format system logs.
3. `/app/httplib.h` - A C++ single-header HTTP library for your convenience.

Your task is to:
1. Extract the instructions from the audio file. It will tell you three things:
   - The specific character encoding used in `system_metrics.bin`.
   - The window size (N) for a rolling average calculation.
   - The TCP port number you must use to serve your results.
2. Read and decode `/app/system_metrics.bin` using the encoding specified in the audio. The file contains comma-separated values in a wide format: `timestamp,zone_alpha,zone_beta,zone_gamma`.
3. Reshape this data from wide format to long format. The resulting logical structure should be `timestamp, zone_name, value`.
4. For each distinct zone, compute an N-period rolling average of the `value` (where N is the window size from the audio). The rolling average at time T should include the value at time T and the N-1 preceding values. If fewer than N values are available, compute the average over the available values.
5. Write a C++ program (using C++17 or later) that performs all of the above processing and spins up an HTTP server (you may use `/app/httplib.h`) listening on `127.0.0.1` at the port specified in the audio.
6. The server must expose an endpoint `GET /rolling?zone=<zone_name>` (e.g., `/rolling?zone=zone_alpha`).
7. The endpoint must return `text/csv` with the exact header `timestamp,value,rolling_avg` and the sorted chronologically computed data for that specific zone. Values should be rounded to 2 decimal places.

Compile your C++ server, run it in the background, and ensure it is actively listening on the correct port before completing the task. You are free to use tools like `whisper.cpp`, `ffmpeg`, or Python for the initial audio transcription to find the parameters, but the data processing and serving MUST be implemented in C++.