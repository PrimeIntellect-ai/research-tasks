You are a data scientist building a spatial model fitting pipeline. You need to analyze a 2D spatial domain, calculate the variance of observational data within grid cells, and refine the grid in areas of high variance.

Your task:
1. Write a C program `/home/user/model_fit.c` that reads observational data, performs domain decomposition, and applies one level of mesh refinement based on a variance threshold.
2. The input data is located at `/home/user/observations.csv`. It contains a header `x,y,v` followed by comma-separated floating-point values. The spatial domain for both `x` and `y` is strictly `[0.0, 1.0]`.
3. Your C program must accept exactly two command-line arguments: `N` (an integer representing the initial `N x N` grid size) and `T` (a float representing the population variance threshold).
4. **Domain Decomposition (LEVEL 1):** Divide the `[0.0, 1.0] x [0.0, 1.0]` domain into an `N x N` grid of equal-sized cells. 
   - Iterate over the grid using an outer loop for the x-axis (index `i` from `0` to `N-1`) and an inner loop for the y-axis (index `j` from `0` to `N-1`).
   - A point `(x, y)` belongs to a cell `[xmin, xmax]` and `[ymin, ymax]` if `xmin <= x < xmax` and `ymin <= y < ymax`. (Exception: for the rightmost and topmost edges of the domain, include points where `x = 1.0` or `y = 1.0`).
   - For each cell, calculate the population variance of the `v` values for all points inside it. If a cell has 0 points, its variance is `0.0`.
5. **Mesh Refinement (LEVEL 2):** If a LEVEL 1 cell has a variance strictly greater than `T`:
   - Immediately print its information to standard output in the format: `LEVEL1,xmin,xmax,ymin,ymax,variance`
   - Then, bisect this cell along both axes to create 4 equal-sized sub-cells.
   - Iterate over these 4 sub-cells using the same outer-x/inner-y loop logic (index 0 to 1).
   - Calculate the population variance for each sub-cell. If a sub-cell's variance is strictly greater than `T`, print: `LEVEL2,xmin,xmax,ymin,ymax,variance`
   - Do not refine further than LEVEL 2.
6. All floating-point values in the output must be formatted to exactly 3 decimal places.
7. **Reproducible Pipeline:** Create a bash script `/home/user/pipeline.sh` that compiles your C program (using `gcc -O3 -lm`), and runs it with `N=2` and `T=2.0`. The script must redirect the standard output of the C program to `/home/user/refined_cells.txt`.
8. Ensure `pipeline.sh` is executable and execute it so that `/home/user/refined_cells.txt` is generated.