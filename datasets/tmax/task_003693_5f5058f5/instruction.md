You are a Machine Learning Engineer tasked with preparing an audio dataset for a Voice Activity Detection (VAD) model. To integrate with our automated data pipeline, you need to build a C++ microservice that performs feature extraction and hyperparameter tuning on raw audio data.

Your goal is to create and run a C++ HTTP server that processes a provided audio file and calculates moving-window metrics. 

Here are the requirements:
1. **Environment Setup**: 
   - You may use single-header libraries like `cpp-httplib` (for the HTTP server) and `nlohmann/json` (for JSON parsing/serialization). Download them as needed.
   - The audio file you will process is located at `/app/dataset_sample.wav`. It is a standard 16-bit PCM Mono WAV file.

2. **C++ Microservice**:
   - Write a C++ program (e.g., `vad_service.cpp`) and compile it.
   - The server must listen on `127.0.0.1:8080`.
   - Implement the following HTTP POST endpoints:
     
     a) `/features/rms`:
        - Accepts a JSON payload: `{"window_ms": <integer>}`.
        - Calculates the Root Mean Square (RMS) amplitude for consecutive, non-overlapping windows of `window_ms` milliseconds from `/app/dataset_sample.wav`.
        - The RMS for a window of $N$ samples is $\sqrt{\frac{1}{N} \sum_{i=1}^{N} s_i^2}$, where $s_i$ is the sample value normalized to the range [-1.0, 1.0] (for 16-bit PCM, divide by 32768.0).
        - Returns a JSON array of floats representing the RMS values for each window. (Drop any final incomplete window).
     
     b) `/tune/threshold`:
        - Accepts a JSON payload: `{"window_ms": <integer>, "threshold": <float>}`.
        - Calculates the RMS for each window (same as above).
        - Returns a JSON object: `{"active_windows": <integer>}`, which is the count of windows where the RMS is strictly greater than `threshold`. This is used to tune the VAD threshold.

3. **Execution**:
   - Compile your C++ code with appropriate flags (e.g., `-std=c++11` or `-std=c++17`, `-lpthread`).
   - Start your server in the background so it remains running.
   - Leave the server running on `127.0.0.1:8080` when you are finished.

Ensure your RMS calculation is numerically accurate and correctly handles the WAV file header (skip the first 44 bytes to read the raw PCM data).