You are an IT support technician responding to an escalated ticket regarding our company's audio processing pipeline. The pipeline has been failing, and we need you to debug the issues, fix the code, and build a robust detection script.

Here is the situation:
1. **Memory Dump Analysis**: The worker node crashed recently, leaving a memory dump at `/app/worker.core`. Our encryption service relies on a 32-character API key that was loaded in memory at the time of the crash. The key is prefixed with the string `API_KEY=`. You must extract this key to decrypt the audio files. Save this key to `/home/user/api_key.txt`.

2. **Concurrency Deadlock**: Our main audio pipeline script at `/app/audio_processor.py` is multithreaded. Under high load, it deadlocks when `process_batch()` is called. Diagnose and fix the race condition/deadlock in this file. You can use system call tracing or logging to identify the locked resources.

3. **Mathematical Convergence Failure**: The script uses a mathematical noise reduction algorithm located in `/app/math_filter.py`. The `denoise_signal()` function uses a custom root-finding algorithm (Newton-Raphson) to map audio frequencies. However, it fails to converge and throws a `RuntimeError` when the derivative approaches zero. Fix the algorithm to repair this convergence failure (e.g., by adding an epsilon or a fallback mechanism) so it successfully processes all valid floating-point inputs without crashing.

4. **Adversarial Detection**: We are being targeted by attackers inserting subtle synthetic anomalies into our audio streams. You are provided with a clean corpus of audio files in `/app/clean/` and an evil corpus containing the anomaly in `/app/evil/`. There is also a reference audio file at `/app/reference_audio.wav` which you can use for baseline profiling. 

Write a Python script at `/home/user/detect_anomaly.py` that takes a single audio file path as a command-line argument. The script must:
- Decrypt the file using the extracted API key (the decryption function is provided in `/app/audio_processor.py`).
- Pass the audio through your fixed `math_filter.py`.
- Output the string `CLEAN` to stdout and exit with code `0` if the audio is clean.
- Output the string `EVIL` to stdout and exit with code `1` if the audio contains the synthetic anomaly.

Your script must correctly classify 100% of the files in `/app/clean/` and `/app/evil/`.