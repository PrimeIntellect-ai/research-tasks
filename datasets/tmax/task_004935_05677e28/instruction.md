You are a data scientist working on extracting physical parameters from acoustic signals. 

We have recorded a damped harmonic oscillator's sound. The audio file is located at `/app/audio/decay_signal.wav`. 

The underlying physics of the sound can be modeled by the equation:
`y(t) = A * exp(-gamma * t) * sin(2 * pi * f * t)`
where `t` is the time in seconds, `A` is the amplitude, `gamma` is the damping coefficient, and `f` is the frequency in Hertz.

Before you can process the data in Python, you need to extract the raw PCM samples into a CSV format. We have a custom high-performance C tool for this, but it needs to be compiled.
1. Navigate to `/app/tools/` where you will find `wav2csv.c`.
2. Compile it from source into an executable named `wav2csv` using `gcc` (it requires no external libraries other than the standard C library).
3. Run the compiled tool on `/app/audio/decay_signal.wav` to produce `/home/user/signal.csv`. The tool takes two arguments: the input WAV file and the output CSV file.

Once you have the CSV file (which contains a single column of normalized floating-point amplitude values, one per sample), write a Python script to fit the theoretical model to the first 4000 samples of the data. The audio sample rate is 8000 Hz. Use an optimization technique (such as gradient descent via `scipy.optimize.curve_fit` or a genetic algorithm like `scipy.optimize.differential_evolution`) to find the optimal parameters `A`, `gamma`, and `f`.

Save your fitted parameters to a JSON file at `/home/user/params.json` with the following exact keys:
`"A"`, `"gamma"`, `"f"`.

Your extraction must be accurate. We will evaluate your parameters by calculating the Mean Squared Error (MSE) between your reconstructed waveform (using your parameters) and the true theoretical waveform over the first 4000 samples.