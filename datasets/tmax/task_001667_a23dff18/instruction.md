You are a performance engineer optimizing an acoustic profiling pipeline. The core pipeline uses Non-negative Matrix Factorization (NMF) on audio spectrograms to separate acoustic sources. However, the pipeline frequently crashes with "near-singular matrix" errors when processing anomalous audio segments—such as perfectly flat signals, pure single-frequency tones, or extreme clipping. 

To fix this, you need to implement a robust pre-filtering pipeline that identifies and rejects these "evil" audio inputs before they reach the NMF step.

**Step 1: Baseline Analysis using Bootstrap**
You have been provided a baseline room recording at `/app/ambient_baseline.wav`.
1. Load the audio file using `scipy.io.wavfile` or `librosa`.
2. Compute the frame-wise Spectral Flatness. 
3. Use bootstrap resampling (with N=5000 iterations) to estimate the 95% confidence interval (using the percentile method, 2.5th and 97.5th percentiles) of the **mean** spectral flatness across all frames in this baseline file.
4. Save this confidence interval as a JSON file at `/home/user/baseline_stats.json` with the format: `{"ci_lower": <float>, "ci_upper": <float>}`.

**Step 2: Adversarial Classifier Optimization**
You must write a Python CLI script at `/home/user/filter.py` that decides whether an audio file is safe to process.
The script must accept exactly one argument (the path to a WAV file):
`python /home/user/filter.py <path_to_wav>`

The script must evaluate the audio file based on two criteria:
1. **Spectral Distribution:** The mean spectral flatness of the file must fall strictly *inside* the 95% confidence interval you computed in Step 1.
2. **Conditioning:** Compute the STFT magnitude matrix of the file (use NFFT=1024, Hop=512, Hann window). Calculate the condition number of this magnitude matrix. Since NMF fails on near-singular inputs, high condition numbers are dangerous. 

You have been provided a training dataset:
- `/app/train/clean/` : Contains examples of valid audio that factorizes successfully.
- `/app/train/evil/` : Contains examples of near-singular/anomalous audio that crashes the pipeline.

You must use an optimization routine (e.g., a simple grid search, simplex, or gradient-free optimization) to find the optimal condition number threshold that perfectly separates the `clean` training set from the `evil` training set, and hardcode this threshold into your `filter.py` script.

**Execution:**
- If the file passes both the baseline CI check and the condition number threshold, your script must exit with code `0` (ACCEPT).
- If the file fails either check, your script must exit with code `1` (REJECT).

Our automated test suite will run your `filter.py` against a hidden test corpus of clean and evil files.