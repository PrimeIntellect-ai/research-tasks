You are a data scientist working on an automated pipeline for fitting models to time-series signals. 
We have a proprietary, stripped black-box binary located at `/app/fit_model` which performs a highly optimized numerical integration and model fitting on input data. It takes a single argument: the path to a NetCDF (.nc) file.

Unfortunately, `/app/fit_model` is highly sensitive to non-physical discontinuities in the data. When given a smooth signal with normal Gaussian noise, it outputs a fitted parameter. When given a signal containing anomalous high-frequency transients, it diverges and prints `ERROR: Divergence detected`.

Your task is to implement a fast, pre-filtering classifier in C to sanitize the data pipeline before it reaches the model fitter. 

Instructions:
1. We have provided a set of 100 unlabeled NetCDF files in `/app/train_data/`. Each file contains a single 1D array of 1000 `double` values under the variable name `"signal"`.
2. Use the black-box binary `/app/fit_model` to determine which of the training files are "clean" (accepted) and which are "evil" (diverged).
3. Analyze the data to find the distinguishing mathematical feature. (Hint: look at the numerical derivatives and compare the variance/distribution between the two classes. Formulate a statistical threshold).
4. Write a C program at `/home/user/detector.c` and compile it to `/home/user/detector`. You will need to use the NetCDF C library (`libnetcdf-dev` is installed, link with `-lnetcdf`).
5. Your executable must take exactly one argument (the path to a NetCDF file) and print exactly `ACCEPT` (followed by a newline) if the file is clean, or `REJECT` (followed by a newline) if it contains anomalies.

Your solution will be evaluated against a held-out test corpus of clean and evil NetCDF files. Your classifier must reject 100% of the evil files and accept 100% of the clean files.