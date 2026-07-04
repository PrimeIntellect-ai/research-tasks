You are a performance engineer working on a bioinformatics application. The Python script `/home/user/analyze.py` performs a Fourier transform on a genomic sequence to find structural periodicities. It reads a FASTA file (`/home/user/data.fasta`), converts the sequence into a numeric array (Purines A/G -> 1.0, Pyrimidines C/T -> -1.0), and computes the Fast Fourier Transform (FFT).

However, the current native Python FASTA parsing is too slow for production. 

A developer has written a fast C parser located at `/home/user/parser.c`, which reads a FASTA file and writes the numerical values directly to a binary file of 32-bit floats (`float` in C). 

Your task is to:
1. Compile the C parser from source into an executable at `/home/user/parser` (e.g., using `gcc`).
2. Update `/home/user/analyze.py` to replace the slow native Python parsing. Your updated script must use the compiled `/home/user/parser` executable to process `/home/user/data.fasta` into a binary file, and then load the 32-bit floats using `numpy` for the FFT. (The C executable takes two arguments: the input FASTA file path and the output binary file path).
3. Compute the FFT, find the index of the maximum absolute magnitude (ignoring the DC component at index 0), and find the magnitude at that peak.
4. Save the results to `/home/user/result.json`.

The `/home/user/result.json` file must be in the following exact JSON format:
```json
{
    "peak_index": <integer>,
    "peak_magnitude": <float rounded to 1 decimal place>
}
```

Ensure the Python script successfully runs with the C executable and produces the correct result.