You are an AI assistant helping a bioinformatics analyst who is processing genomic sequence data to find nucleosome positioning periodicities. 

The analyst maps DNA sequences to a 1D numerical signal (representing GC content) and uses a C++ tool to compute the Fourier transform (FFT) of this signal. The tool then isolates the dominant frequency band and uses gradient descent optimization to fit a Gaussian peak model ($f(x) = A \cdot \exp(-\frac{(x - \mu)^2}{2\sigma^2})$) to the power spectrum to precisely estimate the periodicity density.

Unfortunately, the tool is currently failing. The numerical optimizer in the code diverges due to an incorrectly implemented step-size adaptation (learning rate adjustment), resulting in `NaN` outputs.

Your tasks are:
1. Install the required FFTW3 development libraries (C++) to compile the tool.
2. Inspect the source code located at `/home/user/analyzer.cpp`.
3. Fix the logical error in the step-size adaptation inside the gradient descent loop. The learning rate should *decrease* when the loss increases, and slightly *increase* (or stay the same) when the loss decreases.
4. Compile the fixed C++ program. You must link against the FFTW3 library.
5. Run the program, which will automatically read `/home/user/signal.txt`.
6. Ensure the program creates a file exactly at `/home/user/peak_params.csv` containing a single line with the comma-separated optimized parameters in this exact order: `Amplitude,Mean_Frequency,Variance` (i.e., $A, \mu, \sigma^2$).

Do not modify the initial parameter guesses or the loss function calculation, only the learning rate adaptation logic and parameter update steps.