You are a bioinformatics analyst working with sequencing coverage data. We have been encountering non-reproducible results in our downstream curve-fitting pipelines because the data arrays are reduced (summed) in non-deterministic orders across parallel threads, leading to floating-point accumulation differences. 

To create a reproducible baseline for our regression tests, we need you to compute a stable "top-tier coverage sum" using basic command-line utilities.

You are provided with an HDF5 file containing simulated sequencing coverage data at `/home/user/coverage.h5`. The file contains a single 1D dataset named `/coverage` consisting of floating-point numbers.

Please perform the following steps exclusively using standard Linux shell commands, standard text processing tools (like `sort`, `awk`, `head`), and a quick Python one-liner if needed to extract the data (the `h5py` and `numpy` packages are already installed in the system Python):

1. Extract all the floating-point values from the `/coverage` dataset in `/home/user/coverage.h5` and save them, one per line, to a plain text file at `/home/user/raw_coverage.txt`.
2. To ensure a stable reduction order that is immune to initial dataset shuffling, sort these values numerically in strictly descending order. Save this sorted list to `/home/user/sorted_coverage.txt`.
3. Take exactly the top 100 highest values from the sorted list, sum them together using `awk` (using standard double-precision float addition), and write the final sum to `/home/user/top100_sum.txt`. The sum must be formatted to exactly 4 decimal places (e.g., `1234.5678`).

Make sure the final output files (`/home/user/raw_coverage.txt`, `/home/user/sorted_coverage.txt`, and `/home/user/top100_sum.txt`) are exactly where specified.