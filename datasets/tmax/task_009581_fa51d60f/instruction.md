You are acting as a bioinformatics analyst working on sequence representations.

I have a FASTA file located at `/home/user/sequences.fasta` containing several DNA sequences. I need you to convert these sequences into a numerical format, perform a stabilized matrix decomposition, and extract a specific metric.

Please write and execute a script (in Python, R, or Julia) to perform the following steps exactly:
1. Parse the FASTA file `/home/user/sequences.fasta`.
2. For each sequence, calculate the raw count of all 16 possible overlapping dinucleotides (k=2). The overlapping dinucleotides are formed by adjacent characters (e.g., "ATGC" has "AT", "TG", and "GC").
3. Construct a multi-dimensional array (matrix $X$) where each row corresponds to a sequence (in the order they appear in the FASTA) and each column corresponds to a dinucleotide count. The columns MUST be strictly ordered alphabetically: AA, AC, AG, AT, CA, CC, CG, CT, GA, GC, GG, GT, TA, TC, TG, TT.
4. Compute the $16 \times 16$ scatter matrix $A = X^T X$.
5. To ensure numerical stability for the decomposition, add a small regularization term (ridge) to the diagonal: $A_{stab} = A + 10^{-6} I$, where $I$ is the $16 \times 16$ identity matrix.
6. Perform a Cholesky decomposition on $A_{stab}$ such that $A_{stab} = L L^T$, where $L$ is a lower triangular matrix.
7. Calculate the trace of $L$ (the sum of its main diagonal elements).
8. Write ONLY this trace value, rounded to 4 decimal places, to a file named `/home/user/trace.txt`.

Ensure your environment has the necessary libraries installed (e.g., NumPy/SciPy if using Python) and verify your matrix construction is correct.