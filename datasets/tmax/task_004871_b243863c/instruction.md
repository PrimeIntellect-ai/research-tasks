You have been given access to a Git repository located at `/home/user/audio-service` containing the source code for an internal audio processing microservice. The service exposes an HTTP API that accepts an audio file, transcribes it, and calculates the peak frequency of the audio signal. 

Recently, a regression was introduced. The service is now crashing or returning wildly inaccurate frequency values and corrupted transcripts. The regression occurred somewhere in the last 200 commits. 

Your task consists of the following steps:
1. **Bisect the repository** to find the exact commit that introduced the regression. The service should correctly process the test audio file located at `/app/test_audio.wav`. 
2. **Fix the bugs** on the `main` branch. The regression consists of multiple issues introduced simultaneously:
   - An environment misconfiguration where the transcription engine (Whisper) cannot find its model file.
   - A floating-point precision error in the Fast Fourier Transform (FFT) peak frequency calculation (a conversion to a 32-bit float causes precision loss).
   - An off-by-one boundary condition error when chunking the audio for transcription, causing the last chunk to be dropped or duplicated.
3. **Start the fixed service**. The service must be brought up and listen on exactly `127.0.0.1:9090`.

Service Specification:
- The service must expose a POST endpoint at `/api/v1/analyze`.
- It must accept a Bearer token for authentication: `Bearer secret-token-8842`.
- It expects a multi-part form data upload containing the audio file in the field `audio_file`.
- It must return a JSON response in the following format:
  ```json
  {
    "transcript": "The exact spoken text",
    "peak_frequency_hz": 440.05
  }
  ```

Please debug the application, apply the necessary code and configuration fixes, and leave the fixed service running in the background. Write a log file to `/home/user/debugging_report.txt` containing the hash of the commit that originally introduced the bug.