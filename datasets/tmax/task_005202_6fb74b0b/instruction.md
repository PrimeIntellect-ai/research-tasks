You are an on-call engineer, and you just got paged at 3 AM. Our asynchronous audio-fingerprinting service, `audio-sig-processor`, is completely unresponsive in production and leaking resources heavily when jobs are cancelled. 

We have isolated the issue to a newly deployed mathematical transformation step used to generate audio signatures, but the original developer is unreachable. Your goal is to debug and fix the pipeline.

Here is the situation:
1. **Dependency Conflict:** The service in `/home/user/audio_service/` fails to start because of a dependency conflict between `numpy`, `scipy`, and our legacy `audio_core` library. You need to resolve the `requirements.txt` so the environment successfully builds and runs.
2. **Network/Audio Analysis:** We've captured a network trace at `/app/traffic.pcap` containing the exact payload that triggers the lock-up. You need to extract the `audio/wav` file transmitted in the HTTP stream from this pcap. The original raw audio file is also provided at `/app/corrupted_transmission.wav` as a fallback, but the pcap contains the exact metadata needed to trigger the job.
3. **Delta Debugging & Code Comprehension:** The main mathematical routine in `/home/user/audio_service/math_core.py` (which processes the audio arrays) contains a severe numerical instability (a divide-by-zero or precision loss leading to NaNs), which causes the `asyncio` cancellation handlers to infinite-loop, leaking resources. Identify and minimize the exact array input that triggers this.
4. **Implementation Fix:** Fix the Python implementation in `math_core.py`. The function `compute_signature(audio_array: List[float]) -> List[float]` must be strictly bit-exact equivalent to our reference C implementation. 

We have provided a stripped reference binary of the C implementation at `/app/bin/oracle_audio_sig`. To verify your fix, you must write a wrapper script at `/home/user/audio_service/solution.py` that imports your fixed `compute_signature` and can be run via the command line, accepting a space-separated list of floats and printing the resulting floats to standard output.

Fix the Python code to ensure the numerical stability and guarantee its output perfectly matches the oracle binary for any valid floating-point input array. Leave your final runnable implementation at `/home/user/audio_service/solution.py`.