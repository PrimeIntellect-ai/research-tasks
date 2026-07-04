You are helping a researcher fix a numerical simulation pipeline. We are simulating a 1D diffusion process using spectral methods (Fourier transforms). 

There is a vendored Rust crate located at `/app/diffusion_sim`. It uses `rustfft` to solve the 1D heat equation $\frac{\partial u}{\partial t} = \nu \frac{\partial^2 u}{\partial x^2}$ in Fourier space. However, the simulation produces incorrect, sometimes diverging results due to a bug in how the spatial derivatives are computed in the frequency domain.

Your tasks:
1. **Fix the Simulator:** Inspect the source code in `/app/diffusion_sim`. Find and fix the physical/mathematical bug causing the incorrect spectral derivative. The spatial domain length is $L = 2\pi$.
2. **Run the Simulation:** Build and run the fixed simulator. 
   - Set $\nu = 0.1$.
   - The initial condition is $u(x,0) = \sin(x) + 0.5\sin(3x)$.
   - Number of grid points $N = 256$.
   - Simulate from $t=0$ to $t=1.0$.
   - The simulator should output the final spatial array $u(x, 1.0)$ as a JSON array of floats to `/home/user/final_state.json`. You may need to modify the simulator's `main.rs` to write this specific output.
3. **Spectral Analysis Pipeline:** Create a new Rust project at `/home/user/analyzer`. This project must:
   - Read `/home/user/final_state.json`.
   - Perform a Forward FFT on the data.
   - Compute the Power Spectral Density (PSD) of the final state. (PSD here is defined as the squared magnitude of the complex Fourier coefficients, normalized by $1/N^2$).
   - Output the PSD array as a JSON array of floats to `/home/user/spectrum.json`.

Ensure your pipeline is completely reproducible. We will run an automated metric to compare your `/home/user/spectrum.json` to the analytical ground-truth spectrum.