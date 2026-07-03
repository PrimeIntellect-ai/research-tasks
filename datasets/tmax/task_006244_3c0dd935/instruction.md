You are a bioinformatics analyst tasked with estimating RNA-Seq transcript abundances and analyzing a splicing graph based on observed exon coverages.

You have three input files in the `/home/user/` directory:
1. `exons.txt`: Contains exon names and their lengths (in base pairs). Format: `[Exon_ID] [Length]`
2. `transcripts.txt`: Contains transcript names and the comma-separated list of exons they contain. Format: `[Transcript_ID] [Exon_1],[Exon_2],...`
3. `coverage.txt`: Contains the total read coverage observed for each exon. Format: `[Exon_ID] [Observed_Coverage]`

Your tasks are:
1. **Abundance Estimation (Optimization)**:
   The observed coverage $c_i$ of an exon $i$ can be modeled as a linear combination of the abundances of the transcripts that contain it. Specifically, $c_i \approx \sum_{j} A_{ij} t_j$, where $t_j$ is the abundance of transcript $j$, and $A_{ij}$ is the length of exon $i$ if exon $i$ is present in transcript $j$, and $0$ otherwise.
   Construct the matrix $A$ (rows sorted alphanumerically by Exon_ID, columns sorted alphanumerically by Transcript_ID) and the vector $c$ (sorted by Exon_ID).
   Use Non-Negative Least Squares (NNLS) to find the transcript abundances $t \ge 0$ that minimize the residual sum of squares $||A t - c||_2^2$.

2. **Splicing Graph Analysis (Graph Algorithm)**:
   Construct a directed splicing graph where the nodes are the exons. A directed edge exists from exon $X$ to exon $Y$ if they appear consecutively (in that order) in *any* of the transcripts.
   The weight of the edge $X \to Y$ is defined as the absolute difference between their observed coverages: $|c_X - c_Y|$.
   Find the shortest path cost from the source node (the exon that appears first in all transcripts, e.g., `E1`) to the sink node (the exon that appears last in all transcripts, e.g., `E4`) using these weights.

Write a Python script to perform these analyses. The script must output a JSON file located at `/home/user/results.json` containing:
- `"abundances"`: A dictionary mapping each `Transcript_ID` to its estimated abundance, rounded to exactly 2 decimal places.
- `"shortest_path_cost"`: The cost of the shortest path from the source to the sink exon as an integer.

Ensure any necessary Python packages (like `scipy` or `numpy`) are installed in your environment before running your script.