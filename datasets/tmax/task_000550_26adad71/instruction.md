As a data scientist, I need to analyze a noisy video of a pulsing light source to fit a physical model. 

I have a 10-second video located at `/app/blinking.mp4` (30 frames per second). I need you to write a reproducible Bash pipeline script at `/home/user/run_analysis.sh` that does the following:

1. **Signal Extraction (Multi-dimensional manipulation)**: Process the video to extract the average grayscale brightness (luma) for each frame over time. 
2. **Spectral Analysis**: Perform a Fourier Transform on this 1D brightness signal to determine the dominant pulse frequency (in Hz). 
3. **Numerical Integration**: Compute the numerical integral of the brightness signal over the entire 10 seconds using the trapezoidal rule.
4. **Monte Carlo Simulation**: To estimate the uncertainty of our frequency fit, write a Monte Carlo routine that adds synthetic Gaussian noise (mean 0, std dev 5.0) to the extracted brightness signal 100 times, re-computes the dominant frequency for each noisy signal, and calculates the standard deviation of these 100 frequency estimates.

Your script must be entirely executable in Bash (you may use `ffmpeg`, `awk`, `bc`, and inline `python3` for the FFT/math if necessary, but the pipeline logic and Monte Carlo loop must be driven by Bash). 

When run, `/home/user/run_analysis.sh` should output a file `/home/user/output.json` with exactly the following format:
```json
{
  "frequency": <float_dominant_frequency_in_Hz>,
  "integral": <float_total_brightness_integral>,
  "frequency_std": <float_standard_deviation_from_monte_carlo>
}
```

The automated verifier will check the accuracy of your extracted frequency and integral against the ground truth of the video signal.