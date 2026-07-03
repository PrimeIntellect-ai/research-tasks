I am an ML engineer preparing a training dataset for a new protein language model. I have some observational data scattered across bioinformatics formats that needs to be parsed, merged, and reshaped into a reproducible feature set.

I have a directory `/home/user/data/` containing two files:
1. `sequences.fasta`: Contains protein sequences.
2. `structure.pdb`: Contains 3D structural coordinates for some of these proteins.

Write a reproducible Python script at `/home/user/prepare_features.py` that does the following:
1. Parses `/home/user/data/sequences.fasta`. Some sequence IDs might be duplicated; keep only the *first* occurrence of each sequence ID. 
2. Calculates the mean sequence length ($L_{mean}$) across all unique sequences found in the FASTA file.
3. Parses `/home/user/data/structure.pdb`. For each chain ID, count the total number of Alpha-Carbon atoms (atom name exactly `CA`).
4. Finds the intersection of sequence IDs (from the FASTA) and chain IDs (from the PDB). Note: Sequence IDs in the FASTA are the headers without the `>` (e.g., `>A` means ID is `A`).
5. For each matching ID in the intersection, calculate the difference between its sequence length and the global mean sequence length ($Length - L_{mean}$).
6. Outputs a JSON file to `/home/user/features.json` containing the reshaped data for the matching IDs. 

The JSON should be structured exactly like this:
```json
{
  "A": {
    "ca_count": 5,
    "length_diff_from_mean": 1.5
  },
  "B": {
    ...
  }
}
```

You may use standard libraries or install `biopython` via pip if you prefer. Ensure your script is reproducible and the output JSON keys are sorted alphabetically. Execute your script to generate `/home/user/features.json` before finishing.