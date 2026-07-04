You are a data analyst tasked with building an end-to-end algorithmic ETL and modeling pipeline in C. You have been provided with an audio file containing acoustic telemetry data at `/app/audio/signal.wav`. You also have a corresponding labels file at `/app/data/labels.csv` which contains engagement metrics for specific time windows.

Your objective is to extract acoustic features, merge them with the labels, compute a statistical correlation model, and serve the result via a custom TCP server.

Step 1: Audio Feature Extraction (ETL & Algorithmic Implementation)
Write a C program (e.g., `pipeline.c`) that reads `/app/audio/signal.wav`. The file is guaranteed to be a standard uncompressed RIFF WAV file (16-bit PCM, Mono, 16000 Hz sample rate). 
Your program must parse the WAV header, then process the audio data in non-overlapping 1-second windows (16,000 samples per window). For each window, calculate the Root Mean Square (RMS) amplitude of the 16-bit integer audio samples.
Output these features to `/home/user/rms_features.csv` with the format: `window_index,rms_value` (starting with `window_index` 0).

Step 2: Model Training and Evaluation 
The provided file `/app/data/labels.csv` has the format `window_index,click_rate`. 
Extend your C program to load this CSV, merge it with your computed RMS features by `window_index`, and compute the Pearson correlation coefficient ($r$) between the `rms_value` and the `click_rate` across all available windows. 
You must implement the numerical computation yourself in C (you may use `<math.h>`).

Step 3: Network Service (Multi-Protocol Delivery)
Your C program must then act as an experiment tracking server. It should bind to `127.0.0.1` on port `9000` as a TCP server.
When a client connects, the server must:
1. Wait for an authentication message ending in a newline. The required token is EXACTLY: `AUTH: ds_agent_2024\n`
2. If the token is incorrect, immediately close the connection.
3. If the token is correct, wait for the command `GET_CORRELATION\n`.
4. Respond with the computed Pearson correlation coefficient formatted to exactly four decimal places, followed by a newline (e.g., `RESULT: 0.7654\n`), and then close the connection.

Compile your C program using standard tools (e.g., `gcc pipeline.c -o pipeline -lm`) and run it in the background so it is actively listening on port 9000. 
Do not use any external dependencies other than the standard C library.