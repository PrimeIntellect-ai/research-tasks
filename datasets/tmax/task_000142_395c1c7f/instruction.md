You are an AI assistant helping a computational chemistry researcher. The researcher wants to estimate the excluded volume (van der Waals volume) of a small molecule using a parallel Monte Carlo simulation.

I have placed a PDB file at `/home/user/molecule.pdb`.

Your task is to write and execute a Python script `/home/user/mc_volume.py` that does the following:
1. **Bioinformatics Parsing**: Parse `/home/user/molecule.pdb` to extract the coordinates (X, Y, Z) and element symbols of all `ATOM` records. 
   - Use standard PDB fixed-width columns: X is 31-38, Y is 39-46, Z is 47-54. The element symbol is at columns 77-78 (strip any whitespace).
2. **Setup**: Assign van der Waals radii based on the element:
   - 'C': 1.7 Å
   - 'O': 1.5 Å
   - 'N': 1.55 Å
   - 'H': 1.2 Å
3. **Bounding Box**: Determine the bounding box of the molecule. The minimum X coordinate of the box should be `min(X_atoms) - max(radii) - 2.0`, and the maximum X should be `max(X_atoms) + max(radii) + 2.0`. Apply the same logic for Y and Z.
4. **Parallel Monte Carlo Simulation**: Use `multiprocessing` to run a Monte Carlo volume estimation across 4 parallel worker processes. 
   - Generate a total of `N = 2,000,000` uniform random points inside the bounding box (500,000 per process).
   - Use multi-dimensional array operations (e.g., NumPy) within each worker to efficiently check how many points fall inside *any* atom's sphere (distance from point to atom center $\le$ atom radius).
   - The estimated volume is `Box_Volume * (Total_Points_Inside / Total_Points)`.
5. **Output**: Write the final estimated volume to `/home/user/volume_estimate.txt` exactly in this format:
   `Estimated Volume: <value>` (rounded to 2 decimal places).

Write the script, run it, and ensure the output file is generated correctly.