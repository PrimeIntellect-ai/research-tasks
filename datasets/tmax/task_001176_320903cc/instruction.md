You are a bioinformatics analyst tasked with evaluating a set of newly engineered protein sequences. We want to quantify the difference in local property peaks between two groups of sequences. 

You have been provided with a FASTA file at `/home/user/sequences.fasta` containing sequences belonging to two groups, indicated by the headers (e.g., `>GroupA_1` and `>GroupB_1`).

Please perform the following analysis:
1. **Parse the FASTA file**.
2. **Signal Generation**: Convert each amino acid sequence into a 1D numerical signal. Use a 1-based alphabetical index for the 20 standard amino acids (A=1, C=2, D=3, E=4, F=5, G=6, H=7, I=8, K=9, L=10, M=11, N=12, P=13, Q=14, R=15, S=16, T=17, V=18, W=19, Y=20).
3. **Signal Processing**: Apply a simple moving average filter of window size 3 to smooth the signal for each sequence. Use "valid" mode (do not pad the edges; the resulting signal length should be exactly $L - 2$, where $L$ is the sequence length).
4. **Peak Extraction**: Find the maximum value $M$ of the smoothed signal for each sequence.
5. **Distribution Distance**: Group the $M$ values into two sets corresponding to GroupA and GroupB. Calculate the 1st Wasserstein distance (Earth Mover's Distance) between the empirical distributions of $M$ for GroupA and GroupB.
6. **Output**: Write the calculated Wasserstein distance, rounded to exactly 4 decimal places, to a file named `/home/user/wasserstein.txt`.

You can use any programming language you prefer (Python is recommended, and you can install libraries like `scipy` or `numpy` if needed).