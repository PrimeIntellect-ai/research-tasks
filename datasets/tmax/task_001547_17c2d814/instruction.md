You are an ML engineer preparing acoustic sensor training data for a new anomaly detection model. We have received a 6-second audio recording from an industrial sensor, located at `/app/sensor_stream.wav`.

The recording consists of 6 exactly one-second segments. Each segment contains a dominant acoustic frequency representing a distinct machine state.

Your task is to build a reproducible data preparation pipeline in **Rust** that extracts these states, reshapes them into a specific tensor format, and serves the result via an API for our model orchestration layer.

Specifically, your Rust application must:
1. Read the audio file `/app/sensor_stream.wav`.
2. Segment the audio into 6 equal 1-second chunks.
3. Perform an FFT (Fast Fourier Transform) on each chunk to identify the dominant frequency (the frequency bin with the highest magnitude).
4. Round each dominant frequency to the nearest 100 Hz to categorize the machine state.
5. Reshape this 1-dimensional sequence of 6 categorized frequencies into a 2x3 multi-dimensional array (row-major order).
6. Bring up an HTTP server listening on `127.0.0.1:8080`.
7. Expose a `GET /tensor` endpoint that returns this 2x3 array as a JSON response (e.g., `[[100, 200, 300], [400, 500, 600]]`).

You may use any necessary Rust crates (e.g., `hound` for WAV reading, `rustfft` for FFT, `axum` or `tiny-http` for the server). Please create a new Cargo project in `/home/user/acoustic_pipeline` to implement this.

Once your server is running and ready to serve requests, leave it running in the background or in an active terminal session. Do not terminate the server, as an automated verifier will issue an HTTP request to `http://127.0.0.1:8080/tensor` to validate your pipeline.