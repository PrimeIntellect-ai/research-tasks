You are an AI assistant helping a computational biologist debug and run a structural analysis pipeline. 

The researcher is trying to extract distance matrices from protein structures (PDB format) and perform an LU decomposition on them to analyze structural modes. However, the analysis program `analyze_struct.c` crashes with a "Zero pivot" error because distance matrices have zeros on the diagonal, making them singular or near-singular.

Your task involves debugging the C program, writing output to HDF5, running a convergence test, and performing statistical hypothesis testing.

Here are your specific objectives:

1. **Fix the C code:**
   - The file `/home/user/analyze_struct.c` contains the base implementation.
   - Modify it to accept an optional third command-line argument: a `double` value for `epsilon` (defaulting to 0.0 if not provided).
   - Before performing the LU decomposition, add `epsilon` to all diagonal elements of the distance matrix to regularize it.
   - Modify the C program to write the extracted U-matrix diagonal (an array of doubles, which is returned by `lu_decompose`) into an HDF5 file. The output HDF5 filename should be the second command-line argument. The dataset must be stored at the root of the HDF5 file and be named `/U_diag`.
   - Install any necessary C HDF5 development libraries (e.g., `libhdf5-dev`) and compile the program to `/home/user/analyze_struct`. Make sure to link the math library and HDF5.

2. **Run Convergence Data Generation:**
   - We have two structural states of a peptide in `/home/user/structA.pdb` and `/home/user/structB.pdb`.
   - Run your compiled `/home/user/analyze_struct` on both PDB files using an `epsilon` value of `0.01`.
   - Save the HDF5 outputs to `/home/user/A_eps0.01.h5` and `/home/user/B_eps0.01.h5`.

3. **Statistical Comparison & Visualization:**
   - Write a Python script `/home/user/compare.py` that reads the `/U_diag` datasets from both `A_eps0.01.h5` and `B_eps0.01.h5`.
   - Calculate the Pearson correlation coefficient between the two `U_diag` arrays.
   - Write the Pearson correlation coefficient to a file named `/home/user/correlation.txt`, formatted to exactly 4 decimal places (e.g., `0.1234`).
   - The Python script should also generate a plot comparing the two arrays and save it as `/home/user/plot.png` (the exact plot contents are up to you, as long as the file is created).

Make sure to install any required Python packages (like `h5py`, `scipy`, `numpy`, `matplotlib`) using pip. 
Execute all scripts to produce the final `.h5` files, `correlation.txt`, and `plot.png`.