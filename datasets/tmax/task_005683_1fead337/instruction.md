You are a machine learning engineer preparing a training dataset. We recently updated our preprocessing script to improve performance, but it appears the new version has numerical stability issues on some of our HDF5 data files.

You have a directory of HDF5 files located at `/home/user/ml_data/`.
The old stable preprocessing script is at `/home/user/process_v1.py` and the new, potentially unstable script is at `/home/user/process_v2.py`.

Both Python scripts take a single argument: the path to an HDF5 file. They exit with code `0` on success, and a non-zero exit code if a numerical failure (or any other error) occurs.

Your task is to perform a regression test across the dataset. Find all HDF5 files in `/home/user/ml_data/` where `process_v1.py` successfully processes the file (exit code 0), but `process_v2.py` fails (non-zero exit code).

Write the base names of these failing files (e.g., `data_04.h5`), one per line, sorted alphabetically, into a file at `/home/user/regression_failures.txt`.

You can use any bash commands or write a short bash script to automate this testing.