You are a Machine Learning Engineer preparing a training dataset of time-series sensor signals. The raw data is stored in NetCDF format, but some of the observation files are contaminated by sudden sensor glitches (adversarial/anomalous noise) that will ruin the training process. 

Your task is to build a robust data filter in C to separate the clean data from the anomalous data.

1. **Extract Calibration Criteria:**
   There is a scanned logbook image located at `/app/glitch_criteria.png`. You must use optical character recognition (e.g., `tesseract`) to read the text in this image. It contains the exact `REJECT_THRESHOLD` multiplier used for statistical outlier detection.

2. **Implement the Data Filter:**
   Write a C program located at `/home/user/filter.c` and compile it to `/home/user/filter`.
   The program must:
   - Accept a single command-line argument: the path to a NetCDF file.
   - Read the 1D float array variable named `signal` from the NetCDF file.
   - Compute the mean and the sample standard deviation of the signal.
   - Calculate the maximum absolute deviation from the mean among all points in the signal.
   - If `(max_absolute_deviation / standard_deviation) > REJECT_THRESHOLD` (where REJECT_THRESHOLD is the value you recovered from the image), classify the file as anomalous.
   - Exit with code `0` if the data is clean (preserved/accepted).
   - Exit with code `1` if the data is anomalous (rejected/flagged).

3. **Dependencies:**
   You will need to install the NetCDF C development libraries (`libnetcdf-dev`) to compile your program. Ensure your program is compiled as `/home/user/filter`.

4. **Testing:**
   You are provided with a small sample of test files in `/app/sample_data/`. However, an automated test suite will rigorously evaluate your `/home/user/filter` binary against two hidden corpora: a "clean" dataset and an "evil" (anomalous) dataset. You must ensure your statistical calculations are precise and that your C program correctly interacts with the NetCDF C API.