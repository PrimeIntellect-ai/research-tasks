We have an incident with our internal Voice Command Processing service. Under high load, the multithreaded Python daemon `voice_processor.py` deadlocks and stops responding. 

As an operations engineer triaging this, you need to fix the service. We suspect a recent environment misconfiguration is exacerbating the issue, and the logs have been corrupted.

We have recovered an audio recording (`/app/incident_logs_dictation.wav`) where a frustrated on-call engineer dictated the critical interleaved log events right before the crash, which indicate the race condition sequence.

Your tasks:
1. Transcribe the audio file located at `/app/incident_logs_dictation.wav` to reconstruct the exact timeline of events that leads to the deadlock. Write the reconstructed timeline to `/home/user/reconstructed_timeline.txt`.
2. Fix the environment misconfiguration. The application expects the `PROCESSOR_TMP_DIR` environment variable to be set to a writable directory, but it's currently pointing to a read-only path, causing intermediate validation assertions in the code to silently catch and retry, leading to the deadlock. Ensure the environment is correctly set up so `voice_processor.py` uses `/tmp/voice_processing`.
3. Debug and fix the multithreaded logic in `/home/user/voice_processor.py`. The application takes a list of integer commands from `stdin` and processes them in parallel. Ensure that it no longer deadlocks under contention.
4. Your fixed version of `/home/user/voice_processor.py` must produce the exact same standard output as our reference implementation for any given valid input. It reads a sequence of space-separated integers from `stdin` and outputs processed integers to `stdout`.

Save your final fixed script at `/home/user/fixed_voice_processor.py`.