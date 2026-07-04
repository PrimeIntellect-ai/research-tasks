You are a data scientist analyzing spectroscopic data from a new proprietary instrument. You have been given a raw dataset in HDF5 format located at `/home/user/raw_spectra.h5`. This file contains two 1D datasets: `freq` (frequencies) and `signal` (the measured noisy spectral amplitudes).

The measured `signal` is distorted by both high-frequency noise and the instrument's non-linear frequency response (gain). The measurement model is:
`measured_signal = (true_signal * instrument_gain) + noise`

Your goal is to recover the underlying `true_signal` and save it to a new HDF5 file at `/home/user/recovered_signal.h5` in a dataset named `true_signal`.

To accomplish this, you must complete the following multi-stage workflow:

1. **Compile the De-noising Tool**: 
   There is a source code repository for a scientific filtering tool in `/home/user/spec-filter-src`. Navigate to this directory and compile the software using the provided `Makefile`. This will produce an executable named `spec-filter`.
   The `spec-filter` tool reads a plain text file containing one numeric signal value per line and prints the smoothed signal values to standard output. Pass the raw `signal` through this tool to remove the high-frequency noise.

2. **Query the Instrument Simulator**:
   The instrument's response function (gain) is highly complex and undocumented. However, you have been provided with a compiled, stripped black-box simulator of the instrument at `/app/instrument_oracle`. 
   You can query it in batch mode to get the gain for a list of frequencies:
   `/app/instrument_oracle --batch <input_freqs.txt> <output_gains.txt>`
   The input should be a text file with one frequency value per line, and the output will contain the corresponding gain values.

3. **Recover the Signal**:
   Using the smoothed signal from step 1 and the instrument gain from step 2, invert the measurement model to compute the `true_signal`.

4. **Save the Result**:
   Write a Python script to save the final recovered signal (as a 1D array of floats, the same length as the input) into an HDF5 file at `/home/user/recovered_signal.h5` under the dataset name `true_signal`.

You may write Python scripts and use shell commands to connect these steps. The automated verification system will compare your `true_signal` array to the exact noiseless ground truth using Mean Squared Error (MSE). You must achieve an MSE of less than 0.05.