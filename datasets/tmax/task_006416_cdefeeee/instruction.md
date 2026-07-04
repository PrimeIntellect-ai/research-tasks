You are acting as a bioinformatics software engineer. We need to analyze a protein sequence and its 3D structure to identify periodic hydrophobic patterns and structural clustering.

Create a Rust project in `/home/user/bio_analysis` that reads a sequence and a structure, performs signal processing and graph analysis, and outputs the results as JSON.

Here are the requirements for your Rust application:

1. **Input Files:**
   - FASTA: `/home/user/input/sequence.fasta` (contains a single protein sequence)
   - PDB: `/home/user/input/structure.pdb` (contains the corresponding 3D atomic coordinates)

2. **Hydrophobicity Mapping & Signal Processing (FFT):**
   - Read the sequence from the FASTA file.
   - Map the sequence to a numerical array: Assign `1.0` if the amino acid is Hydrophobic (strictly `A, C, F, I, L, M, V, W, Y`), and `0.0` otherwise.
   - For numerical stability and optimal FFT performance, pad the numerical array with `0.0`s at the end until its length is exactly the next power of 2 (e.g., if length is 46, pad to 64).
   - Compute the Fast Fourier Transform (FFT) of this padded array (you may use the `rustfft` crate).
   - Calculate the magnitude of each complex number in the FFT output.
   - Find the peak frequency strictly greater than 0 (ignore the DC component at index 0). The frequency is calculated as `index / padded_length`. Keep track of this `peak_frequency`.

3. **Graph Algorithms for Structural Clustering:**
   - Parse the PDB file. Extract the X, Y, and Z coordinates for all Alpha-Carbon atoms (lines starting with `ATOM` where the atom name is exactly `CA`). You can assume the CA atoms appear in the exact same order as the residues in the FASTA sequence.
   - Build an undirected graph where the nodes are the *hydrophobic residues* (those with value `1.0` from step 2).
   - An edge exists between two hydrophobic nodes if the Euclidean distance between their CA atoms is strictly less than `7.0` Angstroms.
   - Find the size (number of nodes) of the largest connected component in this subgraph. This is the `largest_hydrophobic_cluster`.

4. **Output:**
   - Ensure the `/home/user/output` directory exists.
   - Write a JSON file to `/home/user/output/results.json` with exactly this structure:
     ```json
     {
       "peak_frequency": 0.125,
       "largest_hydrophobic_cluster": 14
     }
     ```
   - (Round `peak_frequency` to 3 decimal places).

Use standard Cargo to build and run your project. Do not hardcode the expected results; calculate them dynamically.