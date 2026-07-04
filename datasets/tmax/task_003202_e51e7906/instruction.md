You are a data scientist working on an experimental "protein sonification" pipeline that maps amino acid sequences to synthetic spectroscopy signals.

Recently, your team noticed that the simulation produces non-reproducible results across different machines due to floating-point reduction order issues when computing the composite signal. A senior researcher left an audio note explaining the required fix.

Your tasks:
1. Listen to / transcribe the audio note located at `/app/lab_recording.wav`.
2. Follow the instructions in the audio note to implement a bit-exact reproducible script at `/home/user/simulate.py`. The script will be aggressively tested against an oracle with random sequence inputs to verify exact floating-point equivalence.
3. The script will need the frequency mappings provided in `/app/freqs.json`.
4. As requested in the audio, generate the required experimental visualization for the specific sequence mentioned and save it to the specified path. 

Ensure your final Python script `simulate.py` takes a single command-line argument (the raw string sequence) and prints the requested output exactly as specified.