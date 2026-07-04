You are an operations engineer managing an audio-processing microservice environment. One of the microservices relies on a shared filesystem to process incoming audio files, but the normalization worker is currently missing.

Your task is to write a robust Python script that normalizes audio files and integrates with our mock notification system. 

Here are your requirements:
1. Setup the environment: Create directories `/home/user/processed` and `/home/user/reports`.
2. Audio Processing: Write a Python script `/home/user/normalize.py` that reads the audio file located at `/app/input.wav`. The script must normalize the audio such that its peak amplitude is exactly -3.0 dBFS (Decibels relative to full scale). Save the resulting file to `/home/user/processed/output.wav`. You may install and use any Python libraries you need (e.g., `pydub`, `scipy`, `numpy`) or use subprocesses like `ffmpeg`.
3. Notification Configuration: Ensure your script has robust error handling. Upon successful processing of the audio, the script must generate a mock email file at `/home/user/reports/success.eml` with the exact subject line: `Subject: Audio Processed`.
4. Configuration File: As part of our infrastructure monitoring, create a mock configuration file at `/home/user/virtual_fstab` containing exactly this line to simulate a temporary mount for the reports directory:
`none /home/user/reports tmpfs defaults 0 0`

Execute your script so that `/home/user/processed/output.wav` and `/home/user/reports/success.eml` are generated. Our automated verification will evaluate the peak dBFS of your output audio file.