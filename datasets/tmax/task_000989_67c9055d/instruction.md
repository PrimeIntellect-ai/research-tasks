You are a Machine Learning Engineer preparing a climate dataset for training a super-resolution neural network. The raw dataset contains a 2D temperature grid, but due to sensor outages, there is a large spatial block of missing data.

Your task is to write a Go program to read the scientific data, impute the missing values using a parallelized iterative solver, and test for convergence.

Here are the specific requirements:
1. **Setup**: The dataset is provided as a NetCDF4 file at `/home/user/climate_grid.nc`. It contains a single 50x50 2D variable called `temperature`. You may need to install system dependencies (e.g., `libnetcdf-dev`) and initialize a Go module to read it.
2. **Algorithm**: 
   - Missing values in the NetCDF file are represented by the float32 value `-999.0`.
   - Initialize all missing values to `0.0` before beginning the solver.
   - Use the **Jacobi method** (a finite difference relaxation technique) to impute the missing values: in each iteration, update the value of every *missing* cell to be the average of its 4 immediate neighbors (up, down, left, right).
   - Only update cells that were originally missing; the known values are fixed boundary conditions and must not change.
   - You must implement the grid updates using a **parallelized** approach in Go (e.g., using goroutines and `sync.WaitGroup` to compute chunks of the grid concurrently).
3. **Convergence Testing**: 
   - After each full grid update, check for convergence.
   - The algorithm converges when the maximum absolute difference between the old state and the new state for any single cell is less than `1e-4` (`0.0001`).
4. **Output**: Once converged, calculate the sum of all cells in the 50x50 grid. Write this single floating-point value, formatted to exactly 4 decimal places (e.g., `12345.6789`), to a file located at `/home/user/result.txt`.

Write your Go code in `/home/user/impute.go`, build it, and run it to produce the `result.txt` file.