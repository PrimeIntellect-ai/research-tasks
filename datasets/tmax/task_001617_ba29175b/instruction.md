You are an AI assistant helping a bioinformatics analyst debug a sequence processing pipeline written entirely in Bash and Awk.

We are trying to build a basic De Bruijn graph representation (k-mer transition matrix) to help design primers. The script `/home/user/analyze_kmers.sh` is supposed to read a DNA sequence from `/home/user/sequence.fasta`, extract overlapping 3-mers (sliding window of size 3, step size of 1), and count the transitions from one 3-mer to the next (i.e., the 3-mer starting at position `i` transitioning to the 3-mer starting at position `i+1`). 

However, similar to a numerical integrator diverging due to a wrong step-size adaptation, our script is currently "jumping" through the sequence incorrectly, missing overlapping k-mers and causing the resulting network graph to be disjointed and sparse.

Your task:
1. Identify and fix the step-size logic error in `/home/user/analyze_kmers.sh`.
2. Ensure the script correctly populates the 2D associative array to count transitions between adjacent overlapping 3-mers.
3. Modify the script so that, after processing, it prints the transition counts in the format: `KMER1 -> KMER2 : COUNT`. Sort this output alphabetically by `KMER1`, then `KMER2`, and save the complete list to `/home/user/transition_matrix.txt`.
4. Find the single most frequent transition (the one with the highest count). Write just the string of KMER1 and KMER2 separated by a hyphen (e.g., `ATG-TGC`) to `/home/user/top_transition.txt`. If there is a tie, write the one that comes first alphabetically.

Do not use Python or external compiled tools; rely strictly on Bash, Awk, and standard coreutils.

The input sequence file `/home/user/sequence.fasta` is already present on the system.