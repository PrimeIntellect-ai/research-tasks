You are a bioinformatics analyst tasked with analyzing a dataset of DNA sequences. You need to parse a FASTA file, evaluate the numerical stability of two statistical variance algorithms on the sequences' GC content, and generate a text-based visualization of sequence lengths.

You must complete the following phases:

**Phase 1: C Program for FASTA Parsing and Statistical Analysis**
Write a C program at `/home/user/analyzer.c` that reads a FASTA file. The path to the FASTA file should be passed as the first command-line argument.
1. Parse the FASTA file. Headers start with `>`. Subsequent lines until the next header (or EOF) contain the sequence. Ignore newlines within the sequence.
2. For each sequence, calculate the GC content (number of 'G' and 'C' characters divided by the total sequence length).
3. Compute the sample variance of the GC contents across all sequences using two methods:
   - **Method A (Naive Formula):** $s^2 = \frac{\sum (x_i^2) - \frac{(\sum x_i)^2}{N}}{N-1}$ (using `double` precision for accumulators).
   - **Method B (Welford's Online Algorithm):** A numerically stable method using `double` precision.
4. The C program must output exactly three lines to a file named `/home/user/variance_results.txt`:
   - Line 1: `Total sequences: <N>`
   - Line 2: `Naive variance: <value rounded to 8 decimal places>`
   - Line 3: `Welford variance: <value rounded to 8 decimal places>`
5. The C program should also output the length of each sequence, one per line, to a file named `/home/user/lengths.txt`.

Compile your C program into an executable named `/home/user/analyzer` using `gcc`.

**Phase 2: Terminal Visualization**
Write a bash script at `/home/user/plot_hist.sh` that reads `/home/user/lengths.txt` and generates an ASCII histogram of sequence lengths, writing the output to `/home/user/histogram.txt`.
The histogram should have three bins based on sequence length ($L$):
- Bin 1: $L \le 15$
- Bin 2: $15 < L \le 25$
- Bin 3: $L > 25$

The format of `/home/user/histogram.txt` must be exactly:
```
Bin 1: [stars]
Bin 2: [stars]
Bin 3: [stars]
```
Where `[stars]` is a sequence of `*` characters, one for each sequence that falls into that bin.

**Execution**
The input FASTA file is located at `/home/user/data.fasta`. 
Run your compiled C program on this file, then run your bash script to generate the final output files.