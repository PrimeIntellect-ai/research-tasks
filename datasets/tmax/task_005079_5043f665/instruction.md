A data scientist is performing a 1D domain decomposition to estimate the structural density of Alpha-Carbon (`CA`) atoms along the Z-axis of a large protein complex. 

They are encountering an issue: their parallel reduction script aggregates the atomic counts correctly, but spits out the spatial bins in a random order depending on which MPI rank finishes first. When they plot this data, the unordered bins cause the plotting library to draw chaotic, criss-crossing lines, resulting in non-reproducible and unreadable density curves.

Your task is to write a robust Bash pipeline (using standard shell tools like `awk`, `grep`, `sort`, `uniq`, etc.) to parse the PDB file, compute the 1D density histogram, and guarantee a reproducible, sorted reduction order.

Perform the following steps:
1. Read the provided structure file at `/home/user/protein.pdb`.
2. Extract only the lines that begin with `ATOM` and where the atom name (the 3rd whitespace-delimited column) is exactly `CA`.
3. Extract the Z-coordinate, which is located in the 8th whitespace-delimited column.
4. "Decompose" the domain into integer slabs by truncating the decimal portion of the Z-coordinate (i.e., simply remove the decimal point and any digits following it. For example, `4.8` becomes `4`, and `-2.1` becomes `-2`).
5. Calculate the density by counting the number of `CA` atoms that fall into each integer Z-bin.
6. Write the results to `/home/user/z_density.txt`. The file must contain exactly two space-separated columns: `Z_BIN COUNT`.
7. **Crucial:** To fix the plotting reproducibility issue, the final output must be sorted *strictly numerically* by the `Z_BIN` (the first column) in ascending order (lowest/most negative to highest).

The final state of `/home/user/z_density.txt` will be programmatically checked.