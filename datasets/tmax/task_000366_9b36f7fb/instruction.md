You are an ML engineer preparing graph-based training data for a new graph neural network that predicts protein properties. You need to extract geometric graph features and global structural features from protein data.

Your task is to write a C++ program from scratch that processes a protein structure and sequence, calculates graph metrics, performs matrix decomposition, and outputs the features into a specific CSV format. 

Here are the requirements:

1. **Environment Setup:**
   - Download the Eigen library (version 3.4.0) source code to `/home/user/eigen_src` (e.g., from `https://gitlab.com/libeigen/eigen/-/archive/3.4.0/eigen-3.4.0.tar.gz`). Extract it such that the Eigen headers are available for your C++ compilation.
   - You will write your C++ code in `/home/user/workspace/extract_features.cpp`.
   - Compile your program into an executable named `/home/user/workspace/ml_feat_prep`.

2. **Data Inputs:**
   - A PDB file is located at `/home/user/data/protein.pdb`.
   - A FASTA file is located at `/home/user/data/sequence.fasta`.
   
3. **Data Processing (in C++):**
   - **Parse** the PDB file to extract the 3D coordinates (x, y, z) of the Alpha Carbon (`CA`) atoms for each residue.
   - **Parse** the FASTA file and verify that the number of residues in the sequence exactly matches the number of `CA` atoms found in the PDB file. If they do not match, the program should exit with an error.
   - Construct a **Distance Matrix $D$** where $D_{i,j}$ is the Euclidean distance between the `CA` atom of the $i$-th residue and the `CA` atom of the $j$-th residue.
   - Using the Eigen library, perform Singular Value Decomposition (SVD) on the distance matrix $D$. Extract the **top 3 singular values** (the largest 3).
   - Construct a K-Nearest Neighbors (KNN) graph for the residues. For each residue, find its **3 nearest neighbors** based on the Euclidean distance (excluding the residue itself). If there is a tie in distances, favor the smaller index.

4. **Output Generation:**
   - Your C++ program must generate a CSV file at `/home/user/output/features.csv`.
   - **Format Specifications:**
     - The first line must contain exactly the top 3 singular values in descending order, formatted to exactly 4 decimal places, separated by commas. (e.g., `45.1234,12.5678,4.9012`)
     - The subsequent lines must list the 3 nearest neighbors (represented by their 0-based index) for each residue in the order they appear in the PDB. 
     - Format for neighbor lines: `ResidueIndex,NN1_Index,NN2_Index,NN3_Index` (e.g., `0,1,2,3`). Sort the neighbor indices for each row by distance (closest first).
   
Execute your program so that the final output file `/home/user/output/features.csv` is generated successfully. Ensure all directories exist before writing to them.