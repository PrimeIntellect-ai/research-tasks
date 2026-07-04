I am a researcher studying the structural properties of synthetic coiled-coil proteins. We hypothesize that periodic variations in the sequence's physical properties are critical to its stability.

I need you to write a C++ program that analyzes a synthetic protein sequence. 

You will find the sequence in `/home/user/protein.fasta` and a dictionary of amino acid masses in `/home/user/mass_table.txt`.

Your C++ program should do the following:
1. Parse the FASTA file to extract the single protein sequence. Ignore any whitespace or newline characters inside the sequence.
2. Read the mass table, which contains whitespace-separated pairs of `AminoAcid_Char Mass_Value` (e.g., `A 71.0`).
3. Map the protein sequence to a 1D sequence of mass values (let's call this $W[n]$, where $n$ goes from $0$ to $N-1$, and $N$ is the length of the sequence).
4. Compute the total mass of the protein (this is the discrete integral: $\sum_{n=0}^{N-1} W[n]$).
5. Compute the discrete derivative $D[n] = W[n] - W[n-1]$ for $1 \le n \le N-1$, with $D[0] = 0$. Find the maximum absolute value of this derivative.
6. Perform a Discrete Fourier Transform (DFT) on the mass sequence $W[n]$ to find the dominant periodic frequency. Use the `fftw3` library (you will need to install `libfftw3-dev` using `sudo apt-get install`). Calculate the power spectrum $P[k] = |X[k]|^2$ (where $X$ is the FFT output). Find the index $k$ that has the highest power, ignoring the DC component (i.e., search only in $1 \le k \le N/2$).

Once you have written and run your code, save the results to exactly `/home/user/analysis_result.txt` with the following precise format:

```
Total_MW: <value>
Max_Abs_Derivative: <value>
Dominant_Freq_Index: <value>
```

Format `<value>` to exactly one decimal place for the first two (e.g. `75900.0`, `90.0`) and as an integer for the index. Do not add any extra text to this file.