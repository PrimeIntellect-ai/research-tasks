Hello! I am a researcher running acoustic simulations, and I need your help writing a highly optimized 1D wave equation solver in Go. 

I have an audio file located at `/app/pulse.wav` that contains a recorded acoustic pulse. I need you to create a Go program at `/home/user/simulator.go` that does the following:

1. **Read the Initial Condition**: Open `/app/pulse.wav` and read the first 1000 PCM 16-bit audio samples from the first channel. Convert these integer samples to 64-bit floats. This array represents the initial pressure distribution `U` at time `t=0`. Assume the initial velocity is zero, so `U` at `t=-1` is identical to `U` at `t=0`.

2. **PDE Numerical Solving**: Implement a finite difference time-domain (FDTD) solver for the 1D wave equation. 
   The discretized equation is:
   `U[i, t+1] = 2*U[i, t] - U[i, t-1] + (c * dt / dx)^2 * (U[i+1, t] - 2*U[i, t] + U[i-1, t])`
   
   Use Dirichlet boundary conditions where `U[0, t] = 0` and `U[999, t] = 0` for all `t`.

3. **Command-Line Interface**: Your program must accept exactly 4 command-line arguments in this order:
   - `c` (float64): Speed of sound
   - `dt` (float64): Time step size
   - `dx` (float64): Spatial step size
   - `steps` (int): Number of time steps to simulate

4. **Output**: After running the simulation for the specified number of `steps`, the program must print the final state of the 1000 points (from index 0 to 999) to standard output. Each float must be printed on a new line formatted to 6 decimal places (e.g., using `fmt.Printf("%.6f\n", val)`).

Your Go code will be tested against my pre-compiled C reference implementation. It must match the output exactly for various combinations of input parameters. Please compile your Go code to an executable named `/home/user/simulator`.