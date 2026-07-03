You are acting as a bioinformatics analyst. We are studying the Repressilator, a synthetic biological circuit, using a C++ ODE simulation tool located in `/home/user/repressilator`. 

Currently, the tool fails to run correctly. The project relies on an adaptive Runge-Kutta-Fehlberg (RK45) integrator, but the simulation diverges or grinds to a halt because the step-size adaptation logic has a bug (specifically, the ratio used to calculate the new step size is inverted for successful steps, causing the step size to grow when it should shrink or vice-versa).

Your objectives are:
1. **Fix the Integrator:** Locate the bug in the adaptive step-size calculation within `/home/user/repressilator/integrator.cpp` and fix it. The formula for the new step size after a successful step should scale proportional to `(tolerance / error)^0.2`.
2. **Setup Dependencies:** Install any necessary libraries to perform Fast Fourier Transforms in C++ (specifically FFTW3).
3. **Enhance the Simulation:** Modify `/home/user/repressilator/main.cpp` so that after successfully simulating the system from `t = 0` to `t = 1000`:
   - It discards the transient data from `t = 0` to `t = 100`.
   - It interpolates the `p1` protein concentration variable from the adaptive time steps onto a uniform time grid with `dt = 0.1` from `t = 100` to `t = 1000`. (Use simple linear interpolation).
   - It applies a 1D Real-to-Complex FFT (using FFTW3) on this uniform grid data to find the dominant frequency of oscillation of `p1`.
4. **Output:** The modified C++ program should print the dominant frequency (in Hz, meaning cycles per time unit `t`) to a file named `/home/user/result.txt` with exactly 4 decimal places.

To compile the code, you can use `g++` directly. Ensure your final compiled binary is at `/home/user/repressilator/sim` and execute it to generate the result file.

All code should be written in C++. You have `sudo` privileges if you need to install packages using `apt-get`.