You are an assistant helping a researcher set up a reproducible scientific data processing pipeline. 

The researcher has two HDF5 files containing 1D simulation data:
- `/home/user/baseline.h5` (used for testing)
- `/home/user/sim_data.h5` (the new simulation results)

Each HDF5 file contains two 1D datasets of equal length:
1. `time` (time steps in seconds)
2. `T` (temperature readings)

Your task is to build a Bash-centric pipeline that computes the maximum absolute rate of change (numerical derivative) of the temperature with respect to time.

Step 1: Write a script `/home/user/compute_deriv.sh`
- It must take a single argument: the path to an HDF5 file.
- It must extract the `time` and `T` datasets. You may write a brief Python one-liner or short script to extract the data from HDF5 to a temporary plain-text/CSV format, but **the numerical differentiation and reduction must be implemented entirely using Bash and standard UNIX utilities (like `awk`, `sed`, `bc`, etc.)**. Do not compute the derivative in Python.
- Compute the forward difference numerical derivative: `dT/dt = (T[i+1] - T[i]) / (time[i+1] - time[i])` for each adjacent pair of points.
- Find the maximum **absolute** value of `dT/dt`.
- Print this single maximum absolute value to standard output, rounded to exactly 4 decimal places.

Step 2: Create a regression test `/home/user/test_pipeline.sh`
- This script must run `./compute_deriv.sh /home/user/baseline.h5`.
- It should compare the output against the expected value stored in `/home/user/baseline_expected.txt`.
- If the output matches exactly, print "PASS" and exit with code 0.
- If it does not match, print "FAIL" and exit with code 1.

Step 3: Process the simulation data
- Run your pipeline on the simulation data by executing:
  `./compute_deriv.sh /home/user/sim_data.h5 > /home/user/sim_max_deriv.txt`

Ensure that your scripts have execute permissions. You may use `pip install h5py` if you need it for your extraction script.