**IT Support Ticket #8821: Urgent Service Recovery & Audio Extraction**

**Context:**
Our internal asynchronous transcription service (`/app/transcriber_service`) has broken following a recent OS update. The service is designed to process audio streams over a network, but it currently has several critical issues that are preventing us from recovering an important intercepted voicemail.

**Your Objectives:**

1. **Resolve Dependency & Compilation Errors:**
   The service relies on a custom C-extension for audio noise reduction located in `/app/transcriber_service/fast_filter/`. It currently fails to compile and link correctly due to misconfigured linker paths and a dependency conflict in `requirements.txt`. Fix the dependencies and successfully build/install the module.

2. **Fix the Async Memory Leak:**
   The primary script `/app/transcriber_service/main.py` uses `asyncio` to process audio chunks. However, a recent analysis of our logs indicates it leaks task objects whenever a chunk processing is cancelled (which happens frequently due to simulated network drops). Trace the intermediate state of the asyncio event loop and fix the cancellation handling so that tasks are properly awaited and cleaned up.

3. **Analyze Corrupted Network State:**
   The actual audio data we need to transcribe was sent over an unreliable UDP connection. We captured the traffic in `/app/transcriber_service/capture.pcap`. By analyzing the pcap, you will notice a specific repeating sequence of malformed packets. Use this information to determine the XOR key that was inadvertently applied to the audio payload.

4. **Transcribe the Audio:**
   An extracted (but still corrupted/XOR-obfuscated) version of the intercepted audio is located at `/app/voicemail.wav`. 
   - Write a short Python script to repair the audio file using the XOR key you derived from the pcap analysis.
   - Once repaired, use a transcription tool of your choice (e.g., `whisper` via python or CLI) to transcribe the spoken content.

**Deliverables:**
Save the final, plain-text transcript of the repaired audio to:
`/home/user/transcript.txt`

The transcript should contain only the spoken text (punctuation and casing are ignored by our grading system, but the words must be highly accurate). Our automated system will calculate the string similarity metric between your output and the ground truth.