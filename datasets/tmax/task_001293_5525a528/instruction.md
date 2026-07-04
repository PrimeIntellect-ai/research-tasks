You are a bioinformatics analyst tasked with analyzing a set of DNA sequences to find regions of structural transition. You need to identify how nucleotide composition shifts across overlapping sequences by modeling them as a graph and measuring the distance between their probability distributions.

Your task is to write a Go program `/home/user/analyze.go` (and build/run it) that performs the following steps:

1. **Parse the FASTA file:** Read `/home/user/input.fasta`. The file contains multiple DNA sequences with standard FASTA headers (e.g., `>Seq1`).
2. **Build an Overlap Graph:** Construct a directed graph where each node is a sequence. A directed edge exists from Sequence $A$ to Sequence $B$ (where $A \neq B$) if and only if the exact suffix of $A$ of length $K=5$ perfectly matches the exact prefix of $B$ of length $K=5$.
3. **Compute Probability Distributions:** For each sequence, calculate the probability distribution of its single nucleotides (A, C, G, T). The probability is the count of a specific nucleotide divided by the total length of that sequence.
4. **Compute Distance Metrics:** For every directed edge $(A, B)$ in your graph, calculate the Jensen-Shannon Divergence (JSD) between the nucleotide probability distribution of $A$ (distribution $P$) and $B$ (distribution $Q$).
   * Use base-2 logarithms for the Kullback-Leibler divergence.
   * Assume 0 * log2(0) = 0.
5. **Identify Maximum Divergence:** Find the edge that has the maximum JSD value. 
6. **Output the Result:** Write the result to `/home/user/result.txt` in the exact format: `SourceID,TargetID,JSD_Value`. 
   * The IDs should be the FASTA sequence IDs without the `>` character (e.g., `Seq1`).
   * The JSD value must be rounded to exactly 4 decimal places (e.g., `0.1234`).
   * If there are no edges, output `None`. 

**Constraints:**
* Use only the Go standard library.
* Do not use any external dependencies.
* Run your code and ensure `/home/user/result.txt` is created with the final answer.