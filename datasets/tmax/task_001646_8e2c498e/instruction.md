You are a machine learning engineer preparing training data for a surrogate model of a physical system. The raw data comes from a coarse numerical simulation and needs to be refined, converted into a probability distribution, and analyzed before it can be fed into the neural network.

Your task is to write a C program that performs mesh refinement, probability distribution normalization, and statistical distance calculation using the NetCDF C API.

Specifically, write a C program at `/home/user/prepare_data.c` that does the following:
1. **Read Data:** Open a NetCDF file located at `/home/user/input.nc`. Read the 1D double-precision array named `coarse_data` of length $N=100$.
2. **Mesh Refinement:** Create a new array `refined_data` of size $2N - 1 = 199$ using linear interpolation. 
   - Even indices: `refined_data[2*i] = coarse_data[i]`
   - Odd indices: `refined_data[2*i+1] = (coarse_data[i] + coarse_data[i+1]) / 2.0`
3. **Probability Distribution:** Normalize the `refined_data` array so that it sums to 1.0, creating a discrete probability distribution $P$. (Assume all input values are strictly positive).
4. **Distance Metric:** Calculate the Kullback-Leibler (KL) divergence $D_{KL}(P \parallel Q) = \sum_{i=0}^{198} P_i \ln(P_i / Q_i)$ between $P$ and a uniform distribution $Q$ (where $Q_i = 1.0 / 199$ for all $i$). Use the natural logarithm.
5. **Output Data:** Create a new NetCDF file at `/home/user/output.nc`. Save the following:
   - A dimension `n_refined` of size 199.
   - A variable `refined_data` (double, dependent on `n_refined`) containing the interpolated values.
   - A variable `P` (double, dependent on `n_refined`) containing the normalized distribution.
6. **Logging:** Write the computed KL divergence to a text file at `/home/user/result.log` in the exact format: `KL: <value>` (formatted to 6 decimal places, e.g., `KL: 0.123456`).

You will need to install any necessary C development libraries for NetCDF (e.g., `libnetcdf-dev`) to compile your code. You can use standard `gcc` to compile your program.

To complete the task:
1. Ensure the C code is written, compiled, and executed successfully.
2. Verify that `/home/user/output.nc` is created with the correct variables.
3. Verify that `/home/user/result.log` contains the correct KL divergence.