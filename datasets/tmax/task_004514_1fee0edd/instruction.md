You are a bioinformatics analyst tasked with evaluating a sequence complexity metric. We have a C program that calculates local sequence entropy (density of GC content) over a sliding window. However, if the window size (step-size) is too small, the entropy estimation diverges into high-variance noise. 

Your objective is to orchestrate a bash workflow to compile the tool, find a stable window size, process a FASTA dataset, and compare the sequence densities against a reference dataset.

**Step 1: Compilation**
Compile the C source file located at `/home/user/src/seq_density.c` into an executable named `/home/user/bin/seq_density`. 
- The tool reads a single, continuous DNA sequence string (without the `>` header or newlines) from standard input.
- It takes one argument: the window size (integer).
- It outputs one float per line representing the entropy of each window.
*Note: Make sure to link the math library (`-lm`).*

**Step 2: Format Parsing & Window Size Adaptation**
You have a multi-sequence FASTA file at `/home/user/data/input.fasta` (sequences may be wrapped across multiple lines).
Extract the *very first* sequence in the FASTA file. 
Test the following window sizes on this first sequence: `5`, `10`, `20`, `50`.
For each window size, calculate the population variance of the output densities. 
Find the *smallest* window size `W` from the list above where the variance is strictly less than `0.05`.

**Step 3: Density Processing & Reference Comparison**
Using your optimal window size `W`, run the tool on *every* sequence in `input.fasta` (including the first one).
For each sequence, calculate its mean density (the average of all output values from the tool for that sequence).
Compare your calculated mean densities to the reference values provided in `/home/user/data/reference.tsv` (Format: `SeqID\tExpectedMean`).
Calculate the absolute difference between your calculated mean and the expected mean for each sequence.

**Step 4: Reporting**
Identify the `SeqID` of the sequence that has the *largest* absolute difference from the reference.
Create a log file at `/home/user/analysis_report.txt` with exactly two lines in this format:
```
Optimal_W: <W>
Most_Divergent_Seq: <SeqID>
```

Replace `<W>` and `<SeqID>` with your findings.