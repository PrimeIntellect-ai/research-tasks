I need you to recover a linear algebra transformation pipeline from an MLOps voice memo and implement a reproducible numerical script.

A researcher left a voice memo detailing the exact projection matrix used for a specific experiment artifact. The audio file is located at `/app/artifact_summary.wav`.

Your task is to:
1. Transcribe or listen to `/app/artifact_summary.wav` to recover the 3x3 matrix parameters.
2. Write a Python script at `/home/user/transform.py` that takes exactly 3 floating-point numbers as command-line arguments (representing a 3D input vector).
3. The script must apply the transformation matrix specified in the audio to the input vector.
4. Use standard 64-bit floats for all numerical operations to ensure pipeline reproducibility.
5. The script must print the resulting 3D vector to standard output as three space-separated numbers, each strictly rounded to exactly 4 decimal places (e.g., "2.5000 -1.0000 9.6000").

The automated verifier will fuzz your script against an oracle using numerous random input vectors. Your script's output must be bit-exact equivalent to the oracle.