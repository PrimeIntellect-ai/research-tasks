You are a bioinformatics analyst working strictly in a Linux terminal environment. We have a Bash-based pipeline that builds a sequence similarity network by comparing k-mer probability distributions. 

However, our script `/home/user/analyze_network.sh` is crashing on a new dataset `/home/user/sequences.fasta`. The script calculates the L1 distance (Manhattan distance) between the 2-mer probability distributions of every pair of sequences. It then calculates an edge weight as `1.0 / distance`. 

The script is failing because some sequences in the new FASTA file are identical or have exactly the same 2-mer distributions (a "near-singular" input scenario), resulting in a distance of 0 and a subsequent division-by-zero error in `awk`.

Your tasks:
1. **Fix the script:** Modify `/home/user/analyze_network.sh` so that if the distance between two sequences is exactly `0`, the edge weight should be explicitly set to `999.00` instead of calculating `1.0 / distance`. Ensure the script successfully runs to completion.
2. **Generate the Network:** Run the fixed script on `/home/user/sequences.fasta`. The script should output a file `/home/user/edges.tsv` with the format `SeqID1\tSeqID2\tWeight`. 
3. **Data Visualization:** We need to visualize the distribution of these edge weights. Write a new Bash command or script that reads `/home/user/edges.tsv`, rounds the weights to the nearest integer (using standard rounding, e.g., 2.4 becomes 2, 2.5 becomes 3), and creates an ASCII histogram in `/home/user/histogram.txt`.
   - The format of `/home/user/histogram.txt` must be: `[Rounded Weight]: [Asterisks]`
   - Each asterisk `*` represents one edge.
   - Sort the output numerically by the rounded weight in ascending order.
   - Ignore self-comparisons (where SeqID1 == SeqID2) for the histogram.

Constraints:
- You must use Bash, `awk`, `sed`, `grep`, and standard coreutils. Do not use Python, R, or Perl.
- Ensure the output formats exactly match the descriptions.