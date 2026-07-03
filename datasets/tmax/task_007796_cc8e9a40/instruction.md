You are a Machine Learning Engineer preparing baseline feature statistics for a genomic classification model. You need to extract the GC content (the proportion of Guanine and Cytosine nucleotides) from a dataset of DNA sequences and compute a robust confidence interval for the mean GC content across the dataset using a reproducible bootstrap method.

Your task is to write a C++ program that processes a FASTA file, calculates the statistics, and outputs the results.

Here are the exact requirements:
1. Parse the FASTA file located at `/home/user/data/input.fasta`. The file contains multiple sequences, each starting with a header line (beginning with `>`), followed by sequence lines.
2. For each sequence, calculate its GC content (number of 'G' and 'C' characters divided by the total sequence length). Ignore whitespace and newlines when calculating lengths.
3. Compute the sample mean of these GC contents.
4. Perform a custom Bootstrap to find the 95% Confidence Interval (CI) of the mean. To ensure strict reproducibility across compilers, you must implement the following Linear Congruential Generator (LCG) for sampling, rather than using standard library RNGs:
   - Initialize the state: `unsigned long r = 42;`
   - To draw a random index: 
     ```cpp
     r = (r * 1103515245 + 12345) & 0x7FFFFFFF;
     int idx = r % N; // where N is the total number of sequences
     ```
   - Perform exactly `B = 1000` bootstrap iterations.
   - In each iteration, sample `N` indices using the LCG above (update `r` each time), and calculate the mean of the GC contents at those indices.
   - Store the 1000 bootstrap means and sort them in ascending order.
   - The 95% CI lower bound is the value at index `25` (0-indexed array), and the upper bound is at index `975`.
5. The C++ program should be written to `/home/user/process_fasta.cpp`.
6. Compile the program using `g++ -O2 /home/user/process_fasta.cpp -o /home/user/process_fasta`.
7. Run the program and write the output to `/home/user/gc_summary.txt`.

The output file `/home/user/gc_summary.txt` must have exactly this format (rounded to 4 decimal places):
```
Sample Mean: 0.XXXX
95% CI: 0.XXXX to 0.XXXX
```