You are a support engineer tasked with analyzing a diagnostic telemetry recording. A customer has provided an audio file at `/app/telemetry.wav` which contains exactly 50 discrete 1kHz tone pulses separated by silence. The peak absolute amplitude of each pulse represents a critical mathematical metric from their system.

A previous engineer left behind a partially complete pipeline:
1. A Python script `/home/user/extract.py` intended to read `/app/telemetry.wav`, extract the peak absolute amplitude of each of the 50 pulses, and write them to `/home/user/parsed_data.txt` (one float per line). However, it has edge-case parsing bugs (it currently fails to accurately isolate pulses and misses negative-phase peaks).
2. A C program `/home/user/compute.c` which reads `parsed_data.txt` and computes the "total energy" (the sum of the squares of all the values). Unfortunately, this program is currently crashing or producing garbage output due to a memory corruption issue (buffer overflow) that only manifests when processing the full customer dataset.

Your task:
1. Debug and fix `/home/user/extract.py` so it accurately extracts all 50 peak amplitudes. You may rewrite it or use libraries like `scipy` and `numpy`.
2. Trace the intermediate state and fix the memory bug in `/home/user/compute.c`.
3. Compile the C program to `/home/user/compute`.
4. Run the full pipeline.
5. Save the final computed numerical value (a single float) into `/home/user/final_result.txt`.

Ensure your extraction logic correctly identifies the maximum absolute value within each distinct burst of audio.