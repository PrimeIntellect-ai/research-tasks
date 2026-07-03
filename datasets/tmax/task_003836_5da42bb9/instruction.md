You are tasked with implementing a critical spectral filtering script for our new data pipeline. 

The lead data scientist left a voice memo at `/app/memo.wav` detailing the specific numerical stability and smoothing rules needed to process the incoming spectral intensity data. You will need to transcribe or listen to this audio file to understand the exact parameters and edge-case handling required for the algorithm (e.g., window sizes, baseline adjustments, and boundary conditions).

Your objective:
1. Transcribe the audio file `/app/memo.wav` to extract the filtering rules. (You may install tools like `ffmpeg` or `whisper` if needed).
2. Write a Bash script at `/home/user/spectral_filter.sh`. 
3. The script must take a sequence of integers as command-line arguments (e.g., `./spectral_filter.sh 10 20 15 5`).
4. The script must apply the exact filtering algorithm described in the audio memo and output the resulting integers on a single line, space-separated.
5. The script must handle sequences of arbitrary length (up to 100 elements) efficiently.

Make sure your script is executable. It will be rigorously tested against an exact reference implementation using random sequences of integers to ensure bit-exact equivalence.