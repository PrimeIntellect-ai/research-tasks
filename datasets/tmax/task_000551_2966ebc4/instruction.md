You are acting as a performance engineer who is debugging a non-reproducible results issue in our acoustic material analysis pipeline. Our distributed application splits acoustic emission data into chunks (domain decomposition), processes them using FFT (spectroscopy), and compares the energy against a reference dataset. However, we've found that standard parallel summation of floating-point values causes tiny non-deterministic variations in the final calculated energy due to floating-point reduction order.

Your task is to implement a robust, reproducible acoustic analysis microservice in Rust. 

You must write a Rust HTTP server that listens on `127.0.0.1:8080`. It should expose a single POST endpoint `/analyze` which accepts and returns JSON. 

The service must analyze an audio file located at `/app/stress_test.wav` (which is a Mono, 16-bit PCM WAV file).

### Request Payload Format
```json
{
  "segment_index": <integer>,
  "total_segments": <integer>,
  "start_freq": <float>,
  "end_freq": <float>,
  "reference_val": <float>
}
```

### Processing Steps required for each request:
1. **Domain Decomposition:** Load the WAV file and convert the 16-bit PCM samples to `f64`. Let the total number of samples be `N`. Calculate `segment_length = floor(N / total_segments)`. Extract the samples corresponding to `segment_index` (0-indexed). The segment starts at `segment_index * segment_length` and has a length of `segment_length`.
2. **Windowing:** Apply a Hanning window to the extracted segment. The window function is `w[n] = 0.5 * (1.0 - cos(2.0 * PI * n / (segment_length - 1) as f64))` for `n = 0` to `segment_length - 1`. Multiply each sample by its corresponding window value.
3. **Spectroscopy (FFT):** Compute the forward FFT of the windowed segment. You should use the `rustfft` crate.
4. **Energy Calculation:** Calculate the energy (magnitude squared, i.e., `re*re + im*im`) of each frequency bin. The frequency of bin `k` is `k * sample_rate / segment_length` (where `sample_rate` is read from the WAV file). 
5. **Band Filtering & Stable Summation:** Identify all frequency bins where `start_freq <= frequency <= end_freq`. Sum the energy of these bins. To guarantee reproducibility and eliminate floating-point reduction order issues, **you must strictly use the Kahan summation algorithm** to accumulate the sum of these filtered bins.
6. **Reference Comparison:** Calculate the absolute difference between the Kahan-summed energy and the provided `reference_val`.

### Response Payload Format
Return a JSON object with the results as 64-bit floats:
```json
{
  "energy": <float>,
  "difference": <float>
}
```

### Setup Instructions
- Initialize a new Rust project in `/home/user/acoustic_service`.
- You may use any standard Rust crates (e.g., `axum`, `warp`, `hound`, `rustfft`, `serde`, `tokio`).
- Ensure the server is running in the background and listening on port 8080 before you consider the task complete. Keep the server running.
- Create a file `/home/user/service_ready.txt` containing the text "READY" once your server is up and ready to receive requests.

Good luck!