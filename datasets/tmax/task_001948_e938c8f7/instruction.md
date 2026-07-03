You are a data engineer tasked with building an ETL pipeline that processes dictated sensor readings and serves statistical summaries over a network protocol.

1. **Audio Transcription & Data Extraction**:
   There is an audio file located at `/app/sensor_dictation.wav`. This file contains a voice dictating a series of temperature readings from a remote weather station. First, you must install the necessary tools (e.g., `whisper.cpp` or equivalent audio processing tools) to transcribe this audio file. The transcription will contain a list of numbers. Extract these numbers into a tabular format (CSV) with a single column `temperature`.

2. **Data Cleaning & Aggregation (in C)**:
   Write a C program that reads the extracted CSV data. 
   - Identify and remove any outliers. An outlier is defined as any value that falls outside of 3 standard deviations from the mean of the dataset.
   - Handle missing or malformed values (e.g., if the transcription contains words like "unknown" or "error") by dropping those rows.
   - Calculate the sample mean and the 95% confidence interval for the mean of the cleaned temperature data. Assume a normal distribution for the confidence interval calculation.

3. **Multi-Protocol Service (in C)**:
   Extend your C program to act as a TCP server listening on `127.0.0.1:9090`. 
   The server must accept incoming TCP connections and respond to the following exact string commands (terminated by a newline `\n`):
   - `GET_MEAN\n`: Respond with the calculated mean, formatted to 2 decimal places (e.g., `Mean: 24.52\n`).
   - `GET_CI\n`: Respond with the 95% confidence interval, formatted to 2 decimal places (e.g., `CI: [23.10, 25.94]\n`).
   - `AUTH mysecrettoken GET_OUTLIER_COUNT\n`: Respond with the integer number of outliers removed (e.g., `Outliers: 2\n`). If the auth token `mysecrettoken` is not present, drop the connection.

Ensure the server runs continuously in the background so it can be verified.