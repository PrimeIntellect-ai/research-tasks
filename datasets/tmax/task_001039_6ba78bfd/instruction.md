You are an engineer investigating a severe memory leak in our long-running audio processing pipeline. The service periodically crashes with out-of-memory (OOM) errors, and log timeline reconstruction indicates the crashes always follow the ingestion of specific, seemingly corrupted audio files.

A senior engineer left a voicemail with crucial findings before going on leave, which you can find at `/app/voicemail.wav`. 

Your tasks are:
1. **Analyze the Voicemail:** Use a transcription tool (like `whisper` or write a quick script using an API/library of your choice) to recover the spoken content of `/app/voicemail.wav`. It contains the exact root cause of the memory bug (a signed integer overflow related to a specific WAV chunk).
2. **Build a Detector:** Write a Python script at `/app/detector.py` that safely inspects audio files without triggering the memory leak, and classifies them as either clean or adversarial based on the rules described in the voicemail.

**Detector Specification:**
Your script must be callable via the command line as follows:
`python3 /app/detector.py <input_directory> <output_json_path>`

- `<input_directory>`: A folder containing multiple `.wav` files.
- `<output_json_path>`: The path where your script must write a JSON file. The JSON must be a single dictionary mapping the base filename (e.g., `audio_01.wav`) to either the string `"REJECT"` (if the file is adversarial/malicious) or `"ACCEPT"` (if the file is benign).

Ensure your script handles standard WAV parsing correctly and implements the exact classification logic derived from the audio artifact. The automated test will verify your detector against hidden testing corpora.