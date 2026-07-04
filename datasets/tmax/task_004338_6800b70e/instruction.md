You are a bioinformatics analyst tasked with finding optimal PCR primers using a novel 1D domain decomposition (mesh refinement) approach on a set of aligned viral genomes.

We have a set of 5 aligned genome sequences of length 1000 bp, located at `/home/user/aligned_sequences.fasta`.

Your task is to implement the following analytical pipeline:

1. **Calculate Conservation:**
   A column (position) in the alignment is considered "conserved" if all 5 sequences have the exact same nucleotide at that position (ignoring case, but assume all are uppercase A, C, G, T).

2. **1D Mesh Refinement:**
   Start with an initial "mesh" of 5 equal domains of length 200 bp: `[0, 200), [200, 400), [400, 600), [600, 800), [800, 1000)`.
   For each domain, calculate its conservation ratio: `(number of conserved columns in domain) / (length of domain)`.
   **Refinement Rule:** If a domain has a conservation ratio $\ge 0.70$ (70%), split it into two equal-sized halves. 
   Apply this rule recursively to all newly created domains until a domain is either $\le 25$ bp in length OR its conservation ratio is $< 0.70$.
   *(Note: 200 bp domains will split into 100 bp, then 50 bp, then 25 bp).*

3. **Primer Selection:**
   Find all "fully refined" domains (those that reached exactly 25 bp in length) that have a conservation ratio $\ge 0.90$.
   - **Forward Primer:** Select the 25 bp domain from this set with the *lowest* start index. The primer sequence is the exact sequence from the FIRST genome (`Seq1`) in this domain (5' to 3').
   - **Reverse Primer:** Select the 25 bp domain from this set with the *highest* start index. The primer sequence is the **reverse complement** of the sequence from the FIRST genome (`Seq1`) in this domain (5' to 3').

4. **Visualization:**
   Create a plot visualizing this process and save it to `/home/user/conservation_mesh.png`. 
   The plot should show:
   - The conservation ratio (e.g., calculated using a sliding window or simply plotting the mesh domain values) across the 1000 bp genome.
   - Vertical lines denoting the boundaries of the final refined mesh domains.
   - Highlight the chosen Forward and Reverse primer regions (e.g., shaded boxes or red bars).

5. **Reporting:**
   Save your final numerical results to `/home/user/analysis_results.json` with the following exact keys:
   - `"num_final_domains"`: Integer representing the total number of domains in the final, fully refined mesh.
   - `"forward_primer"`: String of the 25 bp forward primer.
   - `"reverse_primer"`: String of the 25 bp reverse primer.

Ensure your code is reproducible and all outputs are placed exactly where requested.