You are an ML engineer preparing a structural biology dataset for a new Graph Neural Network model. You have been given a set of raw protein structures in PDB format and their corresponding sequences in a FASTA file. Your goal is to extract structural features while ensuring numerical stability during normalization, and to package this preprocessing step in an isolated environment.

Your task is to:
1. Create a Python virtual environment at `/home/user/prep_env` and install `numpy`.
2. Write a Python script at `/home/user/preprocess.py` that parses the dataset located in `/home/user/raw_data`.
   - The directory `/home/user/raw_data/pdb/` contains several `.pdb` files.
   - The file `/home/user/raw_data/sequences.fasta` contains the amino acid sequences for these PDBs.
3. For each PDB file, your script must:
   - Extract the 3D coordinates (X, Y, Z) of all Alpha-Carbon atoms (atom name `CA`). Ignore all other atoms.
   - Calculate the Center of Mass (CoM) of these CA atoms.
   - Calculate the Euclidean distance of each CA atom from the CoM.
   - Normalize these distances to ensure scale invariance by dividing each distance by the population standard deviation ($\sigma$) of the distances for that specific PDB. 
   - **Numerical Stability Check:** If the standard deviation is extremely small or zero (e.g., if there is only 1 atom), add a small epsilon `1e-8` to the denominator to prevent division by zero or numerical overflow.
4. Output a CSV file at `/home/user/features.csv` with a header row `pdb_id,seq_length,com_x,com_y,com_z,max_norm_dist`.
   - `pdb_id` is the filename without the `.pdb` extension.
   - `seq_length` is the length of the sequence corresponding to that `pdb_id` parsed from the FASTA file.
   - `com_x`, `com_y`, `com_z` are the coordinates of the Center of Mass.
   - `max_norm_dist` is the maximum normalized distance computed in step 3.
   - All float values must be rounded to exactly 4 decimal places. Sort the CSV rows alphabetically by `pdb_id`.

Execute your script using the virtual environment you created to produce the final `/home/user/features.csv`.