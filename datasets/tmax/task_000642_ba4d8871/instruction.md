You are an AI assistant helping a computational physics researcher. The researcher is running numerical simulations of a stiff Ordinary Differential Equation (ODE) system. Unfortunately, the adaptive step-size integrator occasionally fails, leading to unphysical high-frequency numerical artifacts and exponential divergence of the solution.

The researcher has compiled a dataset of simulation outputs, stored as time-series CSV files (with columns `time,value`). We need to build an automated classifier to filter out the corrupted runs. 

The researcher left an audio lab note in `/app/audio/lab_notes.wav` detailing the exact stability thresholds. The note specifies the maximum allowed dominant frequency of the signal and the maximum allowed exponential growth rate of the signal's envelope.

Your task:
1. Transcribe the audio file `/app/audio/lab_notes.wav` to extract the critical thresholds. (You may install tools like `whisper` or `ffmpeg` to achieve this).
2. Write a Bash script `/home/user/evaluate_run.sh` that takes a single argument: the path to a CSV file.
3. The script must analyze the CSV data by:
   - Performing a Fourier transform (spectral analysis) to find the dominant frequency of the `value` signal (ignore the DC component at 0 Hz).
   - Performing curve fitting (regression) to estimate the exponential growth rate $k$ of the signal's amplitude, assuming a model $A e^{kt}$.
4. Compare the extracted metrics against the thresholds dictated in the lab note.
5. If the simulation run exhibits a dominant frequency OR a growth rate strictly greater than the dictated thresholds, the script must exit with code `1` (indicating a divergent/evil run). Otherwise, it must exit with code `0` (indicating a stable/clean run).
6. Your script `/home/user/evaluate_run.sh` will be tested against two sets of CSV files:
   - A "clean" corpus of stable runs.
   - An "evil" corpus of diverging runs.
   It must successfully classify all files in both corpora.

Ensure your script handles standard output and errors cleanly so it can be used in an automated pipeline. You may write helper Python scripts that your Bash script calls, but the primary entry point must be the Bash script `/home/user/evaluate_run.sh`.