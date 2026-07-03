You are an AI assistant helping a data scientist with a model fitting pipeline. We have a noisy periodic signal stored in an HDF5 file, and we need to extract the dominant frequency of its *first derivative* using C++. 

Your task is to write, compile, and run a C++ program that accomplishes this.

Here are the specifications:
1. **Input Data**: The signal is stored in `/home/user/signal.h5`. It contains a single 1-dimensional dataset of double-precision floats named `/voltage`.
2. **Sampling Information**: The signal was sampled with exactly $N=1024$ points at a sampling interval of $\Delta t = \frac{1}{1024}$ seconds.
3. **Processing Steps**:
    - Read the `/voltage` array from the HDF5 file into your C++ program.
    - Compute the numerical first derivative of the signal with respect to time $t$. Use the central finite difference method ($v'_i = \frac{v_{i+1} - v_{i-1}}{2 \Delta t}$) for interior points, and standard forward/backward differences for the first and last points, respectively.
    - Compute the Discrete Fourier Transform (DFT) of the *derivative* array using the FFTW3 library.
    - Calculate the magnitude spectrum from the FFT output and find the dominant frequency (in Hz). The dominant frequency is the frequency corresponding to the maximum magnitude in the positive frequency half of the spectrum.
4. **Output**: Write *only* the dominant frequency (as an integer) to a file located at `/home/user/result.txt`.

You will need to install any necessary development libraries (e.g., HDF5, FFTW3, compiler) using the system package manager before writing and compiling your code. You have full access to execute bash commands, write code, and compile it. 

Begin.