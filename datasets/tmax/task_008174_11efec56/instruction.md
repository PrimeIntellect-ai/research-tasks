You are an AI assistant helping a data scientist with processing and analyzing experimental data.

We have an HDF5 file located at `/home/user/experiment_data.h5` containing spatial temperature measurements from a recent sensor array experiment. 
The file contains three datasets at the root level:
- `/x`: A 1D array of x-coordinates (from 0 to 99).
- `/y`: A 1D array of y-coordinates (from 0 to 99).
- `/temperature`: A 2D array of temperature values (shape 100x100) corresponding to the x and y coordinates. `temperature[i, j]` corresponds to `x[i]` and `y[j]`.

Your task is to:
1. **Domain Decomposition**: Extract the sub-region of the data where $20 \le x \le 30$ and $40 \le y \le 50$.
2. **Mesh Refinement**: The extracted grid has a spatial step of 1.0. Refine this mesh by performing 2D bilinear interpolation to double the resolution (the new step size should be 0.5 for both x and y). The refined bounding box must remain exactly $x \in [20, 30]$ and $y \in [40, 50]$. This should result in a 21x21 grid.
3. **Data Visualization / Export**: Save the 21x21 refined temperature mesh as a CSV file to `/home/user/refined_mesh.csv`. The CSV should have no headers and no row indices, just the 21x21 grid of temperature values formatted to 4 decimal places. The rows should correspond to `x` coordinates and columns to `y` coordinates.
4. **Model Fitting**: Fit a 2D linear plane model to the **refined** data to extract the spatial gradients. The model is: $T(x,y) = a*x + b*y + c$. Calculate the coefficients $a$, $b$, and $c$ using ordinary least squares.
5. Save the fitted coefficients to a text file at `/home/user/fit_results.txt` in the exact format: `a,b,c` (rounded to exactly 2 decimal places, e.g., `1.23,-0.45,10.00`).

You may use Python or any other language/tool you prefer to write scripts to accomplish this. All output files must be placed in `/home/user/`.