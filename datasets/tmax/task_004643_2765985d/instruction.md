You are a performance engineer profiling a mechanical system. A field engineer has dictated a series of time and velocity measurements into an audio log located at `/app/audio/perf_data.wav`. Your goal is to transcribe this audio, extract the data, and build a deterministic Rust tool to analyze the system's kinematics.

Step 1: Scientific Environment Setup
Install necessary tools (e.g., `openai-whisper`, `ffmpeg`) to transcribe the audio file `/app/audio/perf_data.wav`. The audio contains spoken time and velocity pairs. Extract these pairs into a clean CSV format (`time,velocity`).

Step 2: Rust Kinematics Engine
Create a new Rust project at `/home/user/kinematics/`. Write a CLI tool that reads a sequence of comma-separated `t,v` floats from `stdin` (one pair per line) and computes the following:
1.  **Numerical Integration (Distance):** Calculate the total distance traveled using the Trapezoidal rule over the provided points.
2.  **Numerical Differentiation (Acceleration):** Calculate the constant acceleration for each interval $i$ as $a_i = \frac{v_i - v_{i-1}}{t_i - t_{i-1}}$.
3.  **Bootstrap Confidence Interval:** Calculate the 95% bootstrap confidence interval of the *mean acceleration*. 
    *   Use exactly `1000` resample iterations.
    *   Each resample must be drawn with replacement from the calculated $a_i$ array and have the exact same length as the $a_i$ array.
    *   To ensure bit-exact reproducibility, you MUST use `rand_chacha::ChaCha8Rng` (from the `rand_chacha` crate) seeded strictly with the `u64` value `42` (`ChaCha8Rng::seed_from_u64(42)`).
    *   Calculate the mean for each of the 1000 resamples, sort the means in ascending order, and select the 25th element (index `25`) for the lower bound and the 975th element (index `975`) for the upper bound (assuming 0-indexed sorting).

Your Rust program's `stdout` must strictly match this format (values rounded to exactly 4 decimal places):
```
Distance: 12.3456
Accel_CI: [-1.2345, 2.3456]
```

Step 3: Final Integration
Compile your Rust project in release mode. Feed the CSV data you extracted from the audio into your compiled Rust binary via `stdin`, and redirect the exact standard output to `/home/user/audio_analysis.log`.