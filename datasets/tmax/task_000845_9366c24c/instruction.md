You are a performance engineer analyzing the latency of a critical UI thread in a real-time application. You have captured a time-series trace of the thread's event loop latencies. The data exhibits periodic stalling (acting like a complex signal) and a slow, creeping degradation over time. 

A dataset has been provided at `/home/user/ui_latency.csv`. It contains two columns:
1. `timestamp_ms`: The time the event was recorded, in milliseconds. The events are sampled exactly every 1 millisecond.
2. `latency_us`: The latency of the event loop, in microseconds.

Your task is to write a Python script to process this signal data and extract two key profiling metrics:
1. **Dominant Interference Frequency:** Use a Fast Fourier Transform (FFT) to determine the dominant frequency of the latency spikes in Hertz (Hz). You must ignore the DC component (0 Hz).
2. **Latency Drift:** Use linear regression / curve fitting to determine the baseline degradation rate of the application. This is the slope of the linear fit across the entire dataset (change in latency_us per timestamp_ms).

Once you have calculated these values, output the results to a JSON file at `/home/user/analysis.json`. The JSON file must have exactly this structure:
```json
{
  "dominant_freq_hz": <integer_value>,
  "drift_slope": <float_value_rounded_to_4_decimal_places>
}
```

Ensure your frequency is rounded to the nearest integer, and your drift slope is rounded to exactly 4 decimal places. You can use standard data science libraries like `numpy` and `scipy` to accomplish this.