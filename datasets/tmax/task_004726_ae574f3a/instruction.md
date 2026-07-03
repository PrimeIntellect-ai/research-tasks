You are a performance engineer tasked with reverse-engineering and optimizing a bioinformatics script. A researcher left you an audio memo at `/app/specs.wav` detailing the exact mathematical parameters for a sequence analysis tool they need. 

The original, closed-source reference binary is located at `/app/oracle_primer` (which you can run to test inputs, though it is artificially slowed down). You need to write a highly optimized Python equivalent at `/home/user/fast_primer.py`.

Your script must accept exactly one argument (a DNA sequence string consisting of A, C, G, T) and print exactly two lines:
1. The highest "primer score" found for any contiguous substring of the length specified in the audio. The score is calculated as: `(Number of G or C characters) * 2 - (Number of A or T characters)`.
2. The lower and upper bounds of a bootstrap confidence interval for the primer scores of ALL possible contiguous substrings of that length in the input sequence. The bounds should be printed as two comma-separated floats (e.g., `2.0, 5.0`). 

To match the oracle exactly, you must listen to `/app/specs.wav` to extract the correct:
- Primer length
- Bootstrap iteration count
- Numpy random seed
- Confidence interval percentiles (lower and upper)

The automated verifier will randomly generate thousands of DNA sequences and assert that your script's output is bit-exact equivalent to the oracle's output for every sequence. Ensure your Python script `/home/user/fast_primer.py` is executable and includes the correct shebang.