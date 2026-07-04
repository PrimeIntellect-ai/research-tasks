I need you to simulate acoustic wave propagation in a lossy 1D medium (like a long pipe) driven by an audio recording, and analyze the resulting signal attenuation. 

**Physical System:**
The wave equation with damping is given by:
$$ \frac{\partial^2 u}{\partial t^2} + \gamma \frac{\partial u}{\partial t} = c^2 \frac{\partial^2 u}{\partial x^2} $$
Where:
- Wave speed $c = 343.0$ m/s
- Damping coefficient $\gamma = 15.0$ s$^{-1}$
- Domain length $L = 10.0$ m

**Initial and Boundary Conditions:**
- System is initially at rest: $u(x,0) = 0$, $u_t(x,0) = 0$.
- Right boundary is fixed: $u(L,t) = 0$.
- Left boundary is driven by an audio signal: $u(0,t) = S(t)$.

**Source Audio:**
The driving signal $S(t)$ is located at `/app/pulse.wav`. 
- Read this file to get the boundary condition waveform. Normalize the maximum absolute amplitude of the input to 1.0. 
- The total simulation time $T$ should exactly match the duration of the audio file.
- Use a time step $\Delta t$ exactly equal to the audio sampling period.
- Choose a uniform spatial grid $\Delta x$ such that the Courant-Friedrichs-Lewy (CFL) number is approximately 0.9 for stability.

**Tasks:**
1. **Simulation:** Write a Python script to solve the PDE using a standard 2nd-order explicit finite difference scheme in both space and time. Use central differences for the spatial derivative and time derivative, and a backward or central difference for the damping term.
2. **Signal Extraction:** Extract the simulated signal at the receiver location exactly at $x = 5.0$ m. Save this resulting waveform as `/home/user/received_signal.wav` using the same sample rate as the input file. Format as a standard 16-bit PCM WAV (normalize the output array to [-1.0, 1.0] before saving).
3. **Curve Fitting & Regression:** Calculate the maximum absolute amplitude of the wave over the entire time at 5 specific locations: $x \in \{1.0, 2.0, 3.0, 4.0, 5.0\}$. Fit an exponential decay curve $A(x) = A_0 e^{-\alpha x}$ to these peak amplitudes. Save the extracted attenuation coefficient $\alpha$ (a single float value) to `/home/user/attenuation.txt`.
4. **Scientific Code Regression Testing:** Write a `pytest` test file at `/home/user/test_wave.py`. This file must contain a test function that verifies your numerical solver is $\mathcal{O}(\Delta x^2)$ in space. To do this, simulate a simple Gaussian pulse $S(t) = \exp(-1000(t-0.05)^2)$ with $\gamma=0$ and verify that the error decreases by a factor of roughly 4 when the spatial grid resolution is doubled.

Please implement the solution. I will evaluate the accuracy of your `/home/user/received_signal.wav` against a high-resolution reference simulation.