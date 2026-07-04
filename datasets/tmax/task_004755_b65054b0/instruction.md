You are a performance engineer tasked with profiling a 1D heat diffusion algorithm that runs on biological meshes. To establish a baseline, you need to write a Go program that processes a Protein Data Bank (PDB) file, generates a dynamically refined 1D grid, performs numerical integration, and tests for numerical stability.

Write a Go program located at `/home/user/simulate.go` that performs the following steps:

1. **Bioinformatics Format Parsing**:
   - Read a PDB file located at `/home/user/protein.pdb`.
   - Parse all lines starting exactly with the word `ATOM`.
   - Extract the Z-coordinate for each atom. In standard PDB format, the Z-coordinate is located in columns 47-54 (1-indexed). Treat the extracted string as a float64.

2. **Domain Definition & Initial Mesh**:
   - Calculate `Z_min` and `Z_max` from the parsed Z-coordinates.
   - Define a 1D domain starting at `Z_start = math.Floor(Z_min)` and ending at `Z_end = math.Ceil(Z_max)`.
   - Create an initial uniform 1D mesh from `Z_start` to `Z_end` consisting of cells with width `dx = 1.0`. (e.g., if Z_start=0 and Z_end=4, cells are [0,1], [1,2], [2,3], [3,4]).

3. **Mesh Refinement**:
   - Iterate through your initial cells.
   - If a cell *contains* one or more atom Z-coordinates (inclusive of the lower bound, exclusive of the upper bound, except for the very last cell which includes the upper bound), split it into two equal smaller cells (each with width `dx = 0.5`). 
   - Cells without any atoms remain at `dx = 1.0`.

4. **Domain Decomposition**:
   - Split the resulting refined mesh into two domains based on space:
     - Domain 1: All cells whose midpoint is `< (Z_start + Z_end)/2.0`.
     - Domain 2: All cells whose midpoint is `>= (Z_start + Z_end)/2.0`.
   - Count the number of cells in each domain.

5. **Numerical Integration**:
   - Calculate the integral of the function `f(z) = z^2` over your entire refined mesh using the Midpoint Rule.
   - Formula: `Sum( (midpoint_of_cell)^2 * width_of_cell )` across all cells.

6. **Numerical Stability Testing**:
   - A standard explicit finite difference scheme for 1D heat diffusion is stable if `dt <= (dx_min^2) / 2.0`, where `dx_min` is the smallest cell width in the mesh.
   - For a timestep `dt = 0.2`, determine if the simulation would be `STABLE` or `UNSTABLE`.

7. **Output**:
   - The Go program must write the final results to `/home/user/results.txt` exactly in the following format (replace `<...>` with actual computed values formatted to 4 decimal places where applicable, except counts which are integers):
     ```
     Total Atoms: <count>
     Z_min: <Z_min>
     Z_max: <Z_max>
     Domain 1 Cells: <count>
     Domain 2 Cells: <count>
     Integral: <value>
     Stability dt=0.2: <STABLE/UNSTABLE>
     ```

Initialize a Go module in `/home/user`, write the code, and run it to produce `/home/user/results.txt`.