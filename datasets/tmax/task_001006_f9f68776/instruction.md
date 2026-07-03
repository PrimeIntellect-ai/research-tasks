You are a machine learning engineer preparing structural biology data for a 3D graph neural network. You need to extract feature coordinates from a raw PDB (Protein Data Bank) file and calculate the geometric center of the alpha-carbons to normalize your features.

You are provided with a PDB file at `/home/user/protein.pdb`.

Write a Python script (or use shell commands) to process this file and generate a CSV file at `/home/user/features.csv` with the following specifications:
1. Extract the X, Y, and Z coordinates for all Alpha-Carbon atoms (atom name `CA`, typically found at character positions 13-16 in an `ATOM` record).
2. The output CSV must have the header: `X,Y,Z`
3. Following the header, append the X, Y, and Z coordinates of each `CA` atom, one atom per row.
4. The final row of the CSV must contain the geometric center (the mean of X, mean of Y, and mean of Z) of all the extracted `CA` atoms.
5. All numeric values in the CSV must be formatted to exactly 3 decimal places (e.g., `11.639`, `-5.147`, `0.000`).

The standard PDB format specifies coordinate columns as:
- X: characters 31-38
- Y: characters 39-46
- Z: characters 47-54

Ensure your script cleanly handles the fixed-width nature of the PDB format.