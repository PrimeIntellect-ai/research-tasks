You are a bioinformatics analyst processing raw nanopore sequencing signals. Recently, some of our sequencing runs were contaminated with synthetic adversarial noise, and we need to filter them out before downstream analysis. 

Your task is to build a parallelized signal classifier in Python.

First, your Lead PI left an audio note with the specific parameters for the filter. Transcribe the audio file located at `/app/lab_notes.wav`. It contains the name of the optimization algorithm you must use and the precise spectral peak threshold.

Next, write an MPI-enabled Python script named `/home/user/filter_signals.py` that processes a directory of signal files (`.npy` files containing 1D numpy arrays). 
The script should be callable as:
`mpiexec -n <cores> python /home/user/filter_signals.py <input_dir> <rejected_log_file>`

For each `.npy` file in the `<input_dir>`, your script must:
1. Compute the Fast Fourier Transform (FFT) of the signal to get its magnitude spectrum.
2. Use the optimization algorithm mentioned in the audio file to fit a simple exponential background decay curve to the smoothed magnitude spectrum (fitting `A * exp(-B * f) + C`).
3. Subtract the optimized background curve from the magnitude spectrum.
4. If the maximum peak of the background-subtracted spectrum strictly exceeds the threshold mentioned in the audio, classify the signal as "adversarial/corrupted".
5. Write the base filename (e.g., `signal_042.npy`) of every corrupted signal to the `<rejected_log_file>`, one filename per line. Valid signals should NOT be written to this file.

To handle large datasets, your script must use `mpi4py` to distribute the files among the available MPI processes.

You will be evaluated on your script's ability to perfectly distinguish a hidden test set of clean and adversarial signals. Write clean, robust code that properly manages parallel I/O to the log file (e.g., having rank 0 gather the results and write the file).