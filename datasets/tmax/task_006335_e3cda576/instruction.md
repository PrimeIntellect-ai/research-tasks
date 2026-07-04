I am a bioinformatics analyst working with the Resonant Recognition Model (RRM) to analyze protein sequences. I'm trying to find the characteristic frequency of several protein sequences, but my pipeline keeps crashing downstream when it tries to factorize the covariance matrix of the signals (it hits a singular matrix error due to some flat-line signals from unparsed headers).

I need you to write a Bash script at `/home/user/analyze_rrm.sh` that robustly processes the sequences and outputs their peak frequencies directly, bypassing my broken matrix step.

Here is what your script needs to do:
1. Read the FASTA file located at `/home/user/proteins.fasta`.
2. Parse the sequences (ignoring lines starting with `>`, but keep track of the sequence ID, which is the string immediately following `>`).
3. Convert the amino acid sequence into a numerical signal using the Electron-ion interaction potential (EIIP) mapping provided in `/home/user/eiip.tsv`. (Format: `AminoAcid \t Value`).
4. Truncate or pad each numerical signal with zeros so it is exactly 256 points long.
5. Compute the 1D Discrete Fourier Transform (DFT) of this signal. You may call a short inline Python snippet using `numpy` from your bash script to do the math.
6. Calculate the power spectrum (squared magnitude of the FFT) for each signal.
7. Find the index of the maximum power component. *Crucial:* Ignore the DC component (index 0). Only search for the maximum peak in the indices from 1 to 127.
8. Append the result for each sequence to `/home/user/results.txt` in the format: `>SequenceID: PeakIndex` (e.g., `>Seq1: 42`).

Ensure your script handles the FASTA parsing correctly (concatenating multi-line sequences for a single header) before conversion.

Please write and execute the script to generate `/home/user/results.txt`.