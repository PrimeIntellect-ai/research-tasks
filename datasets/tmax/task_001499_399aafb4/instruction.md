You are a bioinformatics analyst tasked with identifying the dominant structural periodicity of a novel synthetic DNA sequence using the Informational Spectrum Method (ISM). 

The sequence is located at `/home/user/sequence.fasta` (which you will need to process). 

Your objective is to write a reproducible Python pipeline that performs the following steps:
1. Parse the DNA sequence from the FASTA file (ignore the header lines starting with `>`).
2. Map the nucleotide string into a numerical signal using the Electron-Ion Interaction Potentials (EIIP) mapping:
   - A = 0.1260
   - C = 0.1340
   - G = 0.0806
   - T = 0.1335
3. Compute the Power Spectrum of this numerical signal using the Fast Fourier Transform (FFT). The Power Spectrum $P[k]$ is defined as the squared magnitude of the FFT: $P[k] = |X[k]|^2$, where $X[k]$ is the FFT of the signal.
4. Identify the dominant frequency $f$ (where $f = k/N$ and $N$ is the length of the sequence) that has the maximum power within the frequency range $0.1 \le f \le 0.4$.
5. Save the results in a JSON file at `/home/user/result.json` with the following format:
   ```json
   {
       "dominant_frequency": 0.3333,
       "peak_power": 123.4567
   }
   ```
   *Round both numerical values to exactly 4 decimal places.*

Ensure your solution is self-contained and handles basic FASTA parsing. You may use `numpy` and `scipy` for the numerical and spectral analysis.