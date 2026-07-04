I am a researcher running numerical simulations of non-linear wave phenomena. I need to build a reproducible pipeline to solve a specific system, but I'm having trouble with the environment setup and the C++ implementation.

Here is the workflow I need you to complete:

1. **Fix the Vendored FFT Package**: 
   I have a vendored, lightweight FFT library located at `/app/minifft-1.2.0`. Unfortunately, its `Makefile` is currently broken and fails to build. I need you to identify the configuration issue in `/app/minifft-1.2.0/Makefile`, fix it, and compile the library so it produces a static archive `libminifft.a`.

2. **Implement the Simulation in C++**:
   In `/home/user/workspace`, write a C++ program named `wave_sim.cpp`. 
   The program must:
   - Generate a discrete signal $y(t) = \sin(2 \pi f_1 t) + 0.5 \cos(2 \pi f_2 t)$ for $t \in [0, 1)$ with $N=1024$ samples. Use $f_1 = 10$ Hz and $f_2 = 25$ Hz.
   - Use the `MiniFFT::forward_transform` function from the fixed `minifft` library (header is at `/app/minifft-1.2.0/include/minifft.h`) to compute the discrete Fourier transform of $y(t)$.
   - Output the magnitude of the first 50 frequency bins (index 0 to 49) to a file named `/home/user/workspace/spectrum.csv`. The CSV should have two columns: `bin_index` and `magnitude`, separated by a comma.

3. **Reproducible Pipeline**:
   Create a bash script at `/home/user/workspace/run_pipeline.sh` that:
   - Compiles `wave_sim.cpp`, statically linking against `/app/minifft-1.2.0/libminifft.a`.
   - Executes the compiled simulation to produce `spectrum.csv`.

Ensure your C++ code includes the necessary headers and correctly handles the complex number structs defined in `minifft.h`. Do not use any external dependencies other than standard C++ libraries and the provided `minifft`.