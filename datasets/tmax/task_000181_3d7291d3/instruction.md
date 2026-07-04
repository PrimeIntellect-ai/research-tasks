You are an ML Engineer preparing an audio dataset for training a specific acoustic event detection model. You need to build a small pipeline that extracts timestamps of specific frequency pulses from a raw audio file and serves this metadata via a local API for the training data loader.

You have an input audio file located at `/app/data/raw_audio.wav`.

Your task involves three main steps:

1. **Signal Processing & Mesh Decomposition (C++)**
   Write a C++ program at `/home/user/detector.cpp` that reads the audio data. Since standard C++ lacks a WAV parser, you may use a shell command (like `ffmpeg`) to first convert the audio to a raw 32-bit float PCM file, or read the WAV file directly if you prefer.
   Your C++ program must analyze the signal to detect "events". An event is defined as a contiguous time window where the energy in the 4000 Hz frequency band dominates. 
   *Implement a domain decomposition approach:* Break the signal into a coarse uniform 1D mesh of 100ms chunks. For chunks exceeding an energy threshold at 4000 Hz, apply a "refinement" step by calculating the exact start and end times at 10ms resolution.
   The program should output a JSON file at `/home/user/events.json` with the following schema:
   ```json
   {
     "events": [
       {"start": 2.01, "end": 2.50},
       {"start": 5.10, "end": 5.32}
     ]
   }
   ```
   (Times should be in seconds, rounded to two decimal places).

2. **Pipeline Orchestration**
   Write a Python script `/home/user/pipeline.py` that orchestrates the workflow:
   - Compiles the C++ program (using `g++`).
   - Prepares the raw PCM data from `/app/data/raw_audio.wav`.
   - Executes the C++ binary to generate `/home/user/events.json`.

3. **Multi-Protocol Data Service**
   As part of `/home/user/pipeline.py` (or a separate script that remains running), start an HTTP server on port `8080` binding to `127.0.0.1`.
   It must expose an endpoint at `GET /api/events` that returns the exact contents of `events.json` with a `Content-Type: application/json` header.

Run your pipeline and ensure the HTTP server is left running in the background so it can be queried by the automated test verifier.