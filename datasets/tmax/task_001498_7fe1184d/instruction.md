You are a machine learning engineer preparing a data processing pipeline for biological sequence and bioacoustics modeling.

We have a legacy audio file containing instructions left by the lead researcher regarding the exact preprocessing steps needed for our new reference dataset. The audio file is located at `/app/instructions.wav`. 

Your task is to:
1. Listen to or transcribe the audio file to extract the exact algorithmic requirements and parameters.
2. Implement the required mathematical data processing algorithm. The algorithm involves calculating a kernel density estimation and a confidence interval for input reference datasets.
3. Write your final implementation in Python at `/home/user/process.py`.
4. Your script must read a sequence of space-separated floating-point numbers from standard input (`stdin`), process them exactly as described in the audio recording, and print the resulting values to standard output (`stdout`).

Your implementation must be robust and bit-exact, as it will be heavily fuzzed against thousands of randomly generated numerical sequences to ensure it precisely matches our internal C++ oracle's output. Any deviation in the output format, rounding, or mathematical formulation will cause the integration tests to fail.

Ensure your script is executable or can be reliably run via `python3 /home/user/process.py`.