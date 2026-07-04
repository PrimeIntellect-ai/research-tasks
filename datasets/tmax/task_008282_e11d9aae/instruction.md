As a machine learning engineer, I am preparing sequence data for a novel neural network architecture that operates in the frequency domain. I have a raw biological dataset but need it transformed into spectral features and stored in an ML-ready format.

I have a FASTA file located at `/home/user/data/sequences.fasta`. 

Please write and execute a Python script (save it to `/home/user/prepare_features.py`) that does the following:
1. Parses the FASTA file `/home/user/data/sequences.fasta`.
2. Converts each sequence into a numerical array using the following mapping: 'A'=1.0, 'C'=2.0, 'G'=3.0, 'T'=4.0, 'N'=0.0.
3. Computes the 1D Discrete Fourier Transform (FFT) of the numerical array. Calculate the absolute magnitudes of the complex FFT output (using `numpy.abs(numpy.fft.fft(...))`).
4. Saves the resulting magnitude arrays into a single HDF5 file located at `/home/user/data/features.h5`. The datasets inside the HDF5 file should be stored at the root level (`/`), and each dataset's name must correspond exactly to the sequence ID from the FASTA file (e.g., if the FASTA header is `>seq1`, the dataset name in HDF5 should be `seq1`).

Requirements:
- Ensure the HDF5 datasets contain `float64` data.
- Do not compress the HDF5 datasets.
- Ensure the Python script runs successfully and generates `/home/user/data/features.h5`.