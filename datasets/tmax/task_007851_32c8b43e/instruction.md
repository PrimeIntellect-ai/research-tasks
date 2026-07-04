You are a performance engineer working with spectroscopy signal processing pipelines. We have a raw spectroscopy dataset and a C program that applies a spatial filter to it, but the processing is too slow and we need to analyze its behavior.

Your task is to profile the C program to find the performance bottleneck and analyze the processed output data using Python.

**Step 1: Profiling the C application**
1. You have a C source file located at `/home/user/process_spectroscopy.c`. It takes two arguments: an input binary file and an output binary file.
2. Compile this program from source. You must enable `gprof` profiling and use the `-O2` optimization flag. Link against the math library. Name the executable `proc_spec`.
3. An input dataset is provided at `/home/user/input.dat` (a 500x500 matrix of 32-bit little-endian floats).
4. Run the compiled executable, passing `/home/user/input.dat` as the input and `/home/user/smoothed.dat` as the output.
5. Use `gprof` on the generated profiling data to determine the name of the function that consumes the most execution time. 

**Step 2: Signal processing analysis**
1. Write a Python script to read the processed output file `/home/user/smoothed.dat` (which is also a 500x500 row-major matrix of 32-bit floats).
2. Compute the 2D Discrete Fourier Transform (2D FFT) of this smoothed data to find the dominant spatial frequencies. 
3. Identify the `(row, col)` index of the maximum amplitude (absolute value) in the 2D frequency domain. 
   * *Note: Ignore the DC component at index `(0, 0)`. If the FFT produces symmetric conjugate peaks, report the peak with the smaller `row` index.*

**Step 3: Reporting**
Create a text file exactly at `/home/user/report.txt` with exactly two lines:
* **Line 1:** The exact name of the bottleneck function identified in Step 1.
* **Line 2:** The row and column indices of the dominant frequency peak identified in Step 2, formatted exactly as `row,col`.

Do not include any other text in the report file.