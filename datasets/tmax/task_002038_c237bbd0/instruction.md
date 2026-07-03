You are an audio data scientist working on cleaning a speech dataset. The raw audio files have been corrupted with significant tonal interference (specific frequencies of noise) and background hiss. 

You have been provided with a validation set to develop your denoising pipeline, and a test set (only noisy version) that you must clean.

Your workspace is located in `/app/`. The data is structured as follows:
- `/app/data/val_noisy.wav`: A speech file corrupted with the noise profile.
- `/app/data/val_clean.wav`: The ground-truth clean version of the validation file.
- `/app/data/test_noisy.wav`: The target speech file you need to clean.

Your objectives are:
1. **Exploratory Analysis**: Analyze `val_noisy.wav` to identify the specific noise frequencies that have been added. 
2. **Experiment Tracking**: Write a script (in any language) that tests different filtering strategies (e.g., notch filters for the tonal noise, bandpass for the hiss). You must track your experiments by calculating the Mean Squared Error (MSE) between your filtered validation outputs and `val_clean.wav`. Save the logs of your trials in `/app/experiments.csv` with columns including your filter parameters and the resulting `mse`.
3. **Pipeline Reproducibility**: Create a shell script `/app/run_pipeline.sh` that takes an input noisy WAV file path and an output WAV file path, and applies your best filtering parameters to it. 
   Usage example: `./run_pipeline.sh /app/data/test_noisy.wav /app/data/test_cleaned.wav`
4. **Final Integration**: Run your pipeline on `test_noisy.wav` to produce `/app/data/test_cleaned.wav`.

**Requirements:**
- The final output `/app/data/test_cleaned.wav` must be a 16-bit PCM WAV file with the same sampling rate as the input.
- You must successfully remove the tonal interference and reduce the background noise to achieve a low MSE against the (hidden) clean test file.
- Your experiment tracking must show at least 5 different parameter combinations tested.

Ensure all file paths and names match exactly what is requested.