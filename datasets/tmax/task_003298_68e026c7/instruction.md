You are an ML Engineer tasked with preparing an acoustic dataset for a predictive maintenance model. You have been given an initial acoustic emission recording from a test engine, located at `/app/engine_test_run.wav`.

The recording contains two things:
1. High-frequency structural vibrations (the primary signal).
2. A spoken calibration code injected into the audio stream by the test operator.

Your workflow consists of extracting features from this audio, handling numerical instabilities, and exposing the cleaned data via a Rust-based microservice for the downstream ML pipeline.

Step 1: Transcription
Extract the spoken calibration code from `/app/engine_test_run.wav`. You may use Python libraries (e.g., `openai-whisper`) via shell commands to obtain the transcript, but the final integration must be served by your Rust application.

Step 2: Signal Processing & Matrix Factorization (Rust)
Write a Rust application that processes the audio data:
- Read the 16-bit PCM WAV file. Convert the samples to 32-bit floats (normalized to -1.0 to 1.0).
- Reshape the 1D audio signal into a 2D matrix $X$ where each row is a non-overlapping frame of exactly 1024 samples. (Discard any remaining samples at the end).
- Compute the Covariance matrix $C = X^T X$ (size 1024x1024). 
- Because the signal is highly periodic, $C$ is near-singular. Perform a Singular Value Decomposition (SVD) on $C$ to extract its singular values. Use the `nalgebra` crate (or similar) to compute this robustly.
- Save a visualization of the first 1024 audio samples (the first frame) as a line plot to `/home/user/frame_plot.png`. You can use the `plotters` crate for this.

Step 3: Statistical Hypothesis Comparison
The downstream pipeline needs to know if the first (largest) singular value is statistically dominant. Compute the ratio $R$ of the largest singular value to the sum of all singular values. The null hypothesis is that the noise is white (uniform energy, $R \approx 1/1024$). 

Step 4: Integration (Multi-protocol Server)
Your Rust application must run an HTTP server on `0.0.0.0:8000`. The verifier will issue requests to this server.
Implement the following endpoints:
- `GET /transcript`: Returns the raw transcribed text as a plain text string.
- `GET /features`: Returns a JSON object: `{"top_singular_value": 123.45, "variance_ratio": 0.98}` (replace numbers with your computed largest singular value and the ratio $R$).
- `POST /hypothesis`: Accepts a JSON payload `{"threshold": 0.5}`. Returns a JSON object `{"reject_null": true}` if your computed ratio $R$ is greater than the provided threshold, and `false` otherwise.

Constraints:
- You must write the HTTP server and matrix operations in Rust.
- Start the server in the background or within a `tmux` session so you can declare completion.
- The server must remain running on port 8000.