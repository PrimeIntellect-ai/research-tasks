You are a data scientist working on modeling the spatial distribution of alpha-carbon (CA) atoms in a protein structure. You need to write a Python script that parses a PDB file, creates an iteratively refined 1D spatial mesh representing radial distance, and solves a nonlinear equation on the resulting density function.

Perform the following steps:
1. Parse the provided PDB file at `/home/user/protein.pdb`. Extract the X, Y, and Z coordinates of all atoms where the atom name is exactly `CA` (Alpha Carbon) and the record type is `ATOM`.
2. Compute the geometric center $C = (\mu_X, \mu_Y, \mu_Z)$ of these CA atoms.
3. Compute the Euclidean distance $D_i$ from $C$ to each CA atom. Let $R_{max}$ be the maximum of these distances.
4. Define a radial density function: $g(r) = \sum_{i=1}^{N} \exp\left(-\frac{(r - D_i)^2}{2}\right)$, where $N$ is the number of CA atoms.
5. **Mesh Refinement:** 
   Start with an initial 1D mesh containing exactly two points: $r_0 = 0.0$ and $r_1 = R_{max}$.
   Perform exactly **4 iterations** of refinement. In each iteration, evaluate $g(r)$ at all current mesh points. For every adjacent pair of points in the sorted mesh $r_j$ and $r_{j+1}$, if the absolute difference $|g(r_{j+1}) - g(r_j)| > 1.0$, insert the midpoint $\frac{r_j + r_{j+1}}{2}$ into the mesh. (All midpoints for an iteration are calculated simultaneously based on the current iteration's mesh, then inserted to form the mesh for the next iteration).
6. **Nonlinear Equation Solving:**
   Using `scipy.optimize.brentq`, find the root $r^*$ of the equation $g(r) - 2.0 = 0$ in the interval $[R_{max}/2, R_{max}]$. 

Save your results in a JSON file at `/home/user/results.json` with the following structure:
```json
{
  "center": [X, Y, Z],
  "R_max": 12.3456,
  "final_mesh_size": 15,
  "root": 8.7654
}
```
Round the coordinates of `center`, `R_max`, and `root` to 4 decimal places. `final_mesh_size` must be an integer representing the total number of points in your mesh after the 4 refinement iterations.

Do not use external libraries other than `numpy` and `scipy`.