You are a bioinformatics analyst tasked with evaluating a custom sequence analysis tool. 

We have a C program located at `/home/user/seq_analyzer.c` that parses DNA sequences from a FASTA file, stores them in a 2D array, and attempts to fit a Gaussian distribution to the sequences' GC-content using an iterative Maximum Likelihood Estimation (MLE) approach. Finally, it computes a Z-score to perform a statistical hypothesis comparison testing whether the population mean GC-content differs from 0.5.

However, the numerical solver is currently diverging and outputting `NaN` or wildly incorrect values. The original author used an iterative gradient ascent method for the density estimation but hardcoded the step-size parameter (`alpha = 0.8`), which causes massive overshooting when the gradient sum scales with the number of sequences `n`.

Your tasks:
1. Inspect `/home/user/seq_analyzer.c`. Fix the step-size adaptation in the density fitting loop. You must scale the step-size `alpha` by dividing it by the number of sequences `n` (i.e., the effective step size should be `0.8 / n`).
2. Compile the fixed program to an executable named `/home/user/seq_analyzer`. (Ensure you link the math library).
3. Run the compiled executable against the dataset located at `/home/user/dataset.fasta`.
4. Redirect the exact standard output of the successful run to `/home/user/analysis_output.txt`.

The output file should contain exactly three lines formatted as:
Fitted Mean: [value]
Fitted Variance: [value]
Z-score: [value]