You are a performance engineer profiling a bioinformatics application that calculates thermal stability from molecular structures. The application processes massive PDB files, but you have noticed that the mean B-factor (temperature factor) output fluctuates slightly across different runs on the cluster. You suspect this non-reproducibility is due to floating-point reduction order variations in parallel sum operations.

To isolate the issue and establish a gold standard, you need to parse a test file and compute the exact statistics using a stable summation algorithm. 

You have a test structure file located at `/home/user/structure.pdb`. 

Perform the following tasks:
1. Parse the standard PDB file to extract the Atom Name (columns 13-16, 1-based) and the B-factor (columns 61-66, 1-based) for all `ATOM` records. Strip any whitespace from the Atom Name.
2. Group the parsed data by Atom Name. You are specifically interested in the `CA` (alpha-carbon) and `CB` (beta-carbon) atoms.
3. Calculate the exact arithmetic mean of the `CA` B-factors. To avoid floating-point reduction errors, you *must* use a precision-preserving algorithm (like Kahan summation or Python's `math.fsum`). Write this exact mean value, formatted to exactly 6 decimal places, to a file named `/home/user/ca_mean.txt`.
4. Perform a statistical hypothesis comparison to check if the B-factors of `CA` atoms significantly differ from `CB` atoms. Conduct a Welch's t-test (two-sided, unequal variances) between the list of parsed `CA` B-factors and `CB` B-factors.
5. Write the resulting p-value of this test, formatted to exactly 6 decimal places, to a file named `/home/user/p_value.txt`.

You may use any programming language (Python, R, Perl, Ruby, etc.) and standard numerical/statistical libraries available. Your solution must handle standard PDB fixed-column formatting accurately.