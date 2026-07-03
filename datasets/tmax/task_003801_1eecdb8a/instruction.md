You are a performance engineer profiling a new signal processing application. The application processes spectroscopy data stored in HDF5 format, using adaptive mesh refinement to perform density estimation of signal peaks. 

You need to write a Bash script to automate the profiling of this application across different mesh refinement levels. 

Here is your setup:
- A Python application is located at `/home/user/analyze_mesh.py`. It takes two arguments: the path to an HDF5 file and an integer representing the mesh refinement level. It prints the estimated density peak to standard output.
- A sample data file is located at `/home/user/data/spectra.h5`. It contains a 1D dataset at the path `/spectroscopy/signal`.
- You have `sudo` privileges if you need to install any system packages (e.g., `hdf5-tools`, `python3-h5py`, `python3-numpy`).

Write a Bash script named `/home/user/profile_pipeline.sh` that performs the following exact steps:
1. Ensure the necessary system tools are available to parse HDF5 metadata from the command line (e.g., `h5dump`).
2. Programmatically determine the number of elements (length) of the dataset `/spectroscopy/signal` in `/home/user/data/spectra.h5` using ONLY command-line tools like `h5dump` and standard bash text processing (do not write a Python script for this step).
3. Create a CSV file at `/home/user/profiling_results.csv` and write the header: `Level,Length,DensityPeak,Time,Rate`
4. For each mesh refinement level in `2, 4, 8, 16`:
   a. Execute the Python application `/home/user/analyze_mesh.py` with the data file and the current mesh level.
   b. Measure the real execution time (in seconds) of the application using the system `/usr/bin/time` command (use the `%e` format).
   c. Capture the density peak output by the application.
   d. Calculate the processing rate (elements per second) as: `Rate = Length / Time`. You may use `awk` or `bc` to compute this to 2 decimal places.
   e. Append the results to `/home/user/profiling_results.csv` in the format: `Level,Length,DensityPeak,Time,Rate`

Constraints:
- The script must be executable (`chmod +x`).
- Do not modify `/home/user/analyze_mesh.py`.
- Ensure `/home/user/profiling_results.csv` contains exactly 5 lines (1 header + 4 data rows) after your script finishes.
- Run the script once to generate the output CSV.