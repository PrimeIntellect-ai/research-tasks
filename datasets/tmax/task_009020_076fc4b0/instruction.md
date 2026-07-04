You are a bioinformatics analyst tasked with adapting numerical "domain decomposition" and "mesh refinement" concepts to 1D genomic sequence analysis. 

Your objective is to write and execute a C program that parses a FASTA file, decomposes the sequence into chunks, refines the region of interest, and performs a localized primer search.

Here are the specific requirements for your C program:
1. Parse the sequence from `/home/user/input.fasta`. Ignore any header lines starting with `>` and remove all newline characters to form a single continuous DNA sequence string.
2. Perform a uniform 1D domain decomposition: divide the entire sequence into exactly 5 equal contiguous chunks. (You can assume the total sequence length is evenly divisible by 5).
3. Identify the chunk with the highest GC content (the total count of 'G' and 'C' characters). If there is a tie, select the chunk with the lowest 0-based index.
4. Perform "mesh refinement" on this specific chunk by splitting it into two equal halves (sub-domains).
5. For *each* of the two sub-domains independently, search for the primer motif `CGT` and count its occurrences. Overlapping motifs within a sub-domain should be counted, but you must NOT count motifs that cross the boundary between the two sub-domains.
6. Write the results to a log file at `/home/user/results.txt`. The file must contain exactly two lines:
   - Line 1: The 0-based index of the chunk that was refined (0 to 4).
   - Line 2: The sum of the `CGT` occurrences found across both refined sub-domains.

You must implement this in C. Write the C code to `/home/user/analyze.c`, compile it using `gcc`, and run it to produce the `results.txt` file.