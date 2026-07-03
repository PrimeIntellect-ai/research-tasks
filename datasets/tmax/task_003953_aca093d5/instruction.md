You are acting as a Data Scientist assistant. We are analyzing spectral signal data, and our current model-fitting pipeline is suffering from numerical stability issues. The results are not reproducible due to floating-point accumulation errors when processing large simulated arrays.

Your task is to write a highly stable Bash script that processes an input spectral signal and computes its probability distribution distance from a theoretical reference model.

Step 1: Extract Model Parameters
We lost the written record of the calibration parameters, but the lead researcher left an audio memo at `/app/experiment_memo.wav`. You must transcribe this audio (tools like `ffmpeg` and `whisper` are available on the system) to find the two parameters of the theoretical Gaussian model: the mean (`mu`) and the standard deviation (`sigma`). 

Step 2: Implement the Evaluation Script
Write a Bash script at `/home/user/fit_spectrum.sh`. This script will be executed with a single argument: the path to a text file containing exactly 10,000 floating-point numbers (one per line). These represent the measured spectrum at frequencies from f=1 to f=10000.

Your script must perform the following pipeline:
1. **Numerical Differentiation:** Compute the absolute discrete derivative of the input signal. For an input array `S`, this is `D[i] = |S[i] - S[i-1]|` for `i` from 2 to 10000. For `i=1`, `D[1] = 0`.
2. **Theoretical Model Generation:** For each frequency `f` (1 to 10000), compute the theoretical reference value `T[f]` using the unnormalized Gaussian formula: `T[f] = exp(-((f - mu)^2) / (2 * sigma^2))`. Use the `mu` and `sigma` you extracted from the audio file.
3. **Distance Metric & Stable Integration:** We need to compute the L1 distance between the differentiated signal `D` and the theoretical model `T`. The distance is the sum of `|D[f] - T[f]|` for all `f` from 1 to 10000.
4. **Numerical Stability:** To solve our floating-point reduction order issues, you MUST implement **Kahan summation** to accumulate this sum. Naive summation will lose precision and fail our strict equivalence tests. You may use `awk` inside your Bash script to perform these calculations, but you must implement the Kahan summation logic explicitly.

Output format:
Your script `/home/user/fit_spectrum.sh` must print ONLY the final computed distance as a floating-point number, rounded to exactly 6 decimal places.

Make sure your script is executable (`chmod +x /home/user/fit_spectrum.sh`). Our automated test suite will run your script against thousands of random input files to verify its bit-exact equivalence and numerical stability compared to our reference implementation.