You are a performance engineer profiling the control software of a newly manufactured oscillating motor. 

We have provided a video recording of the motor in operation at `/app/machine_run.mp4`. 
The motor oscillates at a specific low frequency.

We have also collected performance traces of the control software's latency. These are generated via a Monte Carlo simulation of the system's scheduling queues. Unfortunately, some of the trace files have been tampered with or corrupted by an anomalous background process.
- **Clean Corpus:** `/app/corpus/clean/` contains 50 CSV trace files. These exhibit latency oscillations at the motor's true operating frequency (which you must deduce from the video) plus simulated Monte Carlo noise.
- **Evil Corpus:** `/app/corpus/evil/` contains 50 CSV trace files. These contain the same base signal and noise, but with an injected high-frequency anomaly (a secondary oscillation) caused by the background process.

Each trace is a CSV file with two columns: `time_ms` and `latency_us`. The data is sampled at 100 Hz for 10 seconds.

Your task is to build a robust classifier to filter out the corrupted traces:
1. Analyze `/app/machine_run.mp4` to determine the motor's base operating frequency (in Hz). You can use `ffmpeg` to extract frames and write a script to find the dominant frequency of the visual intensity.
2. Create a Rust project in `/home/user/anomaly_detector/` that compiles to an executable.
3. Your Rust program must take a single command-line argument: the absolute path to a CSV trace file.
4. The program must parse the CSV, apply a Fast Fourier Transform (FFT) using a crate like `rustfft`, and analyze the spectral frequencies.
5. If the trace is clean (only the base motor frequency + noise), the program must exit with status code `0`.
6. If the trace is evil (contains the anomalous high-frequency component), the program must exit with status code `1` (or any non-zero error code).

Requirements:
- Your Rust code must be placed in `/home/user/anomaly_detector/` and build successfully with `cargo build --release`.
- Do not hardcode the file names; your program will be tested on a hidden holdout set of clean and evil traces using the same parameters.
- Ensure your classification logic relies on spectral analysis (FFT) to distinguish between the clean Monte Carlo noise and the injected frequency anomaly.