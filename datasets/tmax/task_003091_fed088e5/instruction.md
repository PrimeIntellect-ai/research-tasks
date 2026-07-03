You are an artifact manager for a binary repository. We have received a suspicious archive named `/app/artifacts.zip`. It is known to contain malicious paths designed to overwrite system files (a "zip slip" attack), but it also contains important data.

Your tasks are:
1. Write a Python script to safely extract `/app/artifacts.zip` into `/home/user/extracted`. You must strictly ignore any file entry in the zip whose resolved path would fall outside the `/home/user/extracted` directory. Do not extract the malicious files to the target directory under a sanitized name; simply skip them entirely.
2. After safe extraction, you will find `metadata.json` and an audio file `transmission.wav` in the extracted directory.
3. The `metadata.json` file contains structured data with keys `message_start_sec`, `message_end_sec`, and `smoothing_window`. 
4. Write a Python script to process the audio file. You must:
   - Crop the audio to the start and end times specified in the JSON.
   - The audio contains high-frequency noise. Apply a simple moving average filter to the audio samples using the `smoothing_window` value. For a window of size $W$, the smoothed value at index $i$ is the average of the original samples from index $i - W + 1$ to $i$ (inclusive). For indices less than $W-1$, compute the average over whatever samples are available from index $0$ to $i$.
   - Save the processed, cropped audio to `/home/user/clean_transmission.wav` using the same sample rate and format as the original.

Ensure your code is robust and your output audio is properly formatted.