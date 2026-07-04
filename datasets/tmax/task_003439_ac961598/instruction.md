You are an AI assistant helping a computational biology researcher with a data processing pipeline. The researcher is running simulations and needs to compare the amino acid frequency distribution of a sequence dataset against the spatial residue composition of a simulated 3D protein structure.

Your objective is to write and execute a C++ program that parses biological data, reshapes the observations into probability distributions, and calculates the Total Variation Distance (TVD) between them.

Here are the specific steps:

1. **Input Data:**
   - `/home/user/sequences.fasta`: A FASTA file containing multiple protein sequences.
   - `/home/user/structure.pdb`: A PDB (Protein Data Bank) file containing the atomic coordinates of a protein structure.

2. **Parsing `sequences.fasta` (Distribution P):**
   - Read all sequences in the FASTA file (ignoring header lines starting with `>`).
   - Count the occurrences of the 20 standard amino acids (using standard 1-letter uppercase codes: A, R, N, D, C, Q, E, G, H, I, L, K, M, F, P, S, T, W, Y, V). Ignore any other characters.
   - Normalize these counts by the total number of standard amino acids found to create probability distribution $P$.

3. **Parsing `structure.pdb` (Distribution Q):**
   - Parse the PDB file and extract standard amino acid residues.
   - To avoid overcounting, only look at lines starting with `ATOM` where the atom name is exactly `CA` (Alpha Carbon, typically found at columns 13-16 in standard PDB format).
   - The residue name is a 3-letter code (columns 18-20). You must map these standard 3-letter codes to their 1-letter equivalents (e.g., ALA -> A, CYS -> C) and count them. Ignore any non-standard 3-letter codes.
   - Normalize these counts by the total number of valid CA atoms found to create probability distribution $Q$.

4. **Distance Calculation:**
   - Calculate the Total Variation Distance (TVD) between $P$ and $Q$.
   - The formula for TVD is: $TVD = 0.5 \times \sum_{i=1}^{20} |P_i - Q_i|$, where $i$ iterates over the 20 standard amino acids.

5. **Output:**
   - Write a C++ program named `/home/user/analyze.cpp`.
   - Compile it using `g++ -std=c++17 -O2 /home/user/analyze.cpp -o /home/user/analyze`.
   - Run the program. It must create a log file at `/home/user/result.txt` containing strictly the calculated TVD formatted to exactly 4 decimal places (e.g., `0.7083`). No other text should be in this file.

Standard mapping reference:
ALA=A, ARG=R, ASN=N, ASP=D, CYS=C, GLN=Q, GLU=E, GLY=G, HIS=H, ILE=I, LEU=L, LYS=K, MET=M, PHE=F, PRO=P, SER=S, THR=T, TRP=W, TYR=Y, VAL=V.