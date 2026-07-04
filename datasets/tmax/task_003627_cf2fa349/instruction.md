I am a computational biology researcher analyzing a simulated protein trajectory. I have a multi-model PDB file representing different snapshots (models) of a peptide over time, and its corresponding FASTA sequence. 

I need you to write a Python script that calculates the Root Mean Square Fluctuation (RMSF) for the alpha-carbon (`CA`) atom of each residue across all models, identifies the residue with the highest RMSF, and cross-references it with the FASTA file to output a final summary.

The files are located at:
- PDB Trajectory: `/home/user/trajectory.pdb`
- Sequence: `/home/user/sequence.fasta`

Please perform the following steps:
1. Parse `/home/user/trajectory.pdb`. This file contains multiple `MODEL` blocks.
2. Extract the 3D coordinates (X, Y, Z) for all atoms named exactly `CA` (Alpha Carbons) for each model. You should represent this as a multi-dimensional array or equivalent structure.
3. Calculate the RMSF for each `CA` atom across all models. The RMSF for atom $i$ is defined as:
   `RMSF_i = sqrt( (1/N) * sum_{n=1}^{N} [ (x_{i,n} - x_{i,avg})^2 + (y_{i,n} - y_{i,avg})^2 + (z_{i,n} - z_{i,avg})^2 ] )`
   where $N$ is the total number of models, $(x_{i,n}, y_{i,n}, z_{i,n})$ are the coordinates of atom $i$ in model $n$, and $(x_{i,avg}, y_{i,avg}, z_{i,avg})$ is the average position of atom $i$ across all models.
4. Identify the residue sequence number (as listed in the PDB file) of the `CA` atom with the maximum RMSF.
5. Parse `/home/user/sequence.fasta` to find the 1-letter amino acid code corresponding to that residue sequence number (assume the PDB residue sequence numbers are 1-based and align perfectly with the 1-based indices of the FASTA sequence).
6. Save the final result to a file named `/home/user/highest_fluctuation.txt` exactly in this format:
   `Residue: <Index> (<Amino_Acid>), Max_RMSF: <Value rounded to 3 decimal places>`
   For example: `Residue: 2 (A), Max_RMSF: 1.253`

You may use standard Python libraries or install packages like `numpy` or `biopython` if you prefer. Ensure your script handles the mathematical calculations precisely.