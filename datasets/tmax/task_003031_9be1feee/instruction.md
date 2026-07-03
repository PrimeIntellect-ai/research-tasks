You are a data scientist analyzing a large dataset of synthetic genomic sequences. A script has generated a FASTA file located at `/home/user/sequences.fasta`. 

Your task is to write a Python script that does the following:
1. Parses the FASTA file `/home/user/sequences.fasta`.
2. Calculates the length ($x$) and the GC content ratio ($y$) for every sequence in the file. The GC content ratio is defined as the total number of 'G' and 'C' characters divided by the sequence length.
3. You must process the sequences in parallel using Python's `multiprocessing` module (e.g., using a `Pool` of 4 worker processes) to speed up the calculation of the GC content.
4. After extracting the lengths and GC content ratios for all sequences, perform a linear regression to fit the model: `GC_ratio = slope * length + intercept`. You can use `scipy` or `numpy` for this curve fitting.
5. Save the results to a file named `/home/user/regression_results.txt`.

The output file `/home/user/regression_results.txt` must have exactly this format:
```
slope: <value>
intercept: <value>
```
Round the `<value>`s to exactly 6 decimal places.

Write and execute the script to complete the task.