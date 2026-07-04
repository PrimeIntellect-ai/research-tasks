You are a performance engineer tasked with profiling a custom scientific C library used for tensor operations. We need to empirically determine the time complexity of the primary function by measuring its execution time across different input sizes and fitting the results to a polynomial complexity model.

Here is what you need to do:

1. **Compile the Library from Source**
   In `/home/user/src/`, there is a C source file named `tensor_ops.c`. Compile it into a shared library named `libtensor.so` in the same directory. Ensure it is compiled with position-independent code (`-fPIC`) and as a shared object.

2. **Write a Profiling Script**
   Create a Python script at `/home/user/profile_ops.py` that does the following:
   * Uses the `ctypes` module to load `/home/user/src/libtensor.so`.
   * Sets up the function signature for `void compute_interactions(double* A, int N)`.
   * Evaluates the execution time of `compute_interactions` for a set of square 2D arrays.
   * For each $N \in \{50, 100, 150, 200, 250\}$:
     * Generates a 2D NumPy array of size $N \times N$ filled with random float64 values between 0.0 and 1.0.
     * Passes a pointer to the array data and the integer $N$ to the C function.
     * Accurately measures the wall-clock execution time of the C function call. (Run it 3 times for each $N$ and take the minimum time to reduce noise).
   
3. **Perform Curve Fitting**
   * Using `scipy.optimize.curve_fit`, fit your empirical timing data to the model: $T(N) = a \cdot N^b$.
   * Estimate the parameters $a$ and $b$. The parameter $b$ represents the empirical exponent of the time complexity.

4. **Export the Results**
   Save the results to `/home/user/profiling_results.json` with the exact following JSON structure:
   ```json
   {
       "N_values": [50, 100, 150, 200, 250],
       "times": [<time_for_50>, <time_for_100>, <time_for_150>, <time_for_200>, <time_for_250>],
       "exponent_b": <estimated_b_rounded_to_2_decimal_places>
   }
   ```