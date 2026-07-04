You are tasked with building a secure, automated ingestion pipeline for an artifact curation system. The system receives binary packages (ZIP archives containing audio artifacts and metadata) and must rigorously filter out corrupted, malicious, or non-compliant files before they are written to the permanent repository.

First, your manager has left you an audio briefing detailing the security requirements for the current batch of artifacts. 
1. Use an appropriate tool (e.g., `whisper.cpp`, `ffmpeg`, or Python libraries like `speechrecognition`/`openai-whisper` which you can install via pip) to transcribe the audio file located at `/app/admin_instructions.wav`. 
2. Listen for the "secret authorization token" spoken in the recording.

Next, write a Python script at `/home/user/ingest_filter.py` that implements the ingestion filter.
The script must accept exactly two arguments:
`python /home/user/ingest_filter.py --input-dir <input_directory> --output-dir <output_directory>`

For every `.zip` file in the `--input-dir`, your script must perform the following checks:
1. **Archive Integrity Verification:** The file must be a valid, uncorrupted ZIP archive.
2. **Metadata Verification:** The archive must contain a file named `metadata.txt`. The first line of this file must be exactly `Token: <SECRET_TOKEN>`, where `<SECRET_TOKEN>` is the token you recovered from the audio briefing.
3. **Binary Header Extraction:** The archive must contain exactly one `.wav` file. Your Python script must manually extract and parse the binary RIFF/WAV header of this file (do NOT use external CLI tools like `ffprobe` for this specific check, read the binary bytes directly). You must verify that the audio is exactly:
   - Audio Format: PCM (Format code 1)
   - Channels: 2 (Stereo)
   - Sample Rate: 44100 Hz
   - Bits per Sample: 16

If a `.zip` file fails *any* of these checks, it must be completely ignored.
If a `.zip` file passes *all* checks, it must be copied to the `--output-dir`. 
**Crucial Requirement:** To prevent race conditions with downstream file watchers, the copy operation must be *atomic*. You must write the file into the `--output-dir` with a `.tmp` extension first, and then rename it to its original `.zip` filename only after the copy is fully complete and the file descriptor is closed.

Ensure your code is robust. We will test `/home/user/ingest_filter.py` against a hidden corpus of clean and malicious/corrupted archives.