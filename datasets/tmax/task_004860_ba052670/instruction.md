You are a performance and simulation engineer working on a large-scale chemical reaction network profiler. We have a pipeline that simulates reaction dynamics on molecular graphs, but it suffers from severe numerical instability when running stiff configurations with our fast explicit solvers.

You need to complete a multi-stage workflow:

**Stage 1: Video Profiling of the Reference Reaction**
We recorded a reference simulation of a 2-node chemical reaction. The video is located at `/app/reaction_video.mp4`. 
- The video consists of 50 frames (at 10 fps, 5 seconds total). 
- It shows two squares side-by-side. The left square is Node A, the right is Node B.
- The intensity of the red channel (0-255) in the center of each square represents the concentration of the chemical at that node over time.
- Extract the frames using `ffmpeg` and parse the red-channel values to get a time-series of concentrations $A(t)$ and $B(t)$.
- The reaction follows the ODE system: 
  $dA/dt = -k \cdot A + c \cdot B$
  $dB/dt = k \cdot A - c \cdot B$
- Estimate the rate constants $k$ and $c$ using ordinary least squares or numerical fitting on the empirical derivatives.
- Perform a bootstrap sampling (N=1000) on the time-series differences to calculate the 95% confidence intervals for $k$ and $c$. 
- Save your findings in `/home/user/reaction_params.json` with the format:
  ```json
  {
    "k_mean": 0.0, "k_ci_lower": 0.0, "k_ci_upper": 0.0,
    "c_mean": 0.0, "c_ci_lower": 0.0, "c_ci_upper": 0.0
  }
  ```

**Stage 2: Graph Configuration Adversarial Filter (C Implementation)**
Our explicit Euler solver (using a fixed time step $\Delta t = 0.1$) often blows up on certain reaction network topologies (stiff systems). 
We have generated two corpora of network configuration files:
- `/app/corpus/clean/`: Contains stable reaction networks.
- `/app/corpus/evil/`: Contains highly stiff networks that cause numerical overflow (NaN/Inf) or explosive oscillations when integrated with $\Delta t = 0.1$.

Each configuration file is a plain text file formatted as follows:
```
N
M_00 M_01 ... M_0(N-1)
M_10 M_11 ... M_1(N-1)
...
```
Where `N` is the number of nodes (integer), and `M_ij` are the reaction rate coefficients (floating-point). The ODE system for the network is $dX/dt = M X$.

Write a C program named `stability_filter.c` in `/home/user/` that acts as a gatekeeper. It must:
1. Accept a single file path as a command-line argument.
2. Read the matrix $M$.
3. Perform a numerical stability test to determine if the explicit Euler integration ($X_{n+1} = X_n + \Delta t M X_n$) with $\Delta t = 0.1$ will be stable or unstable over 1000 steps starting from an initial state of $X_0 = [1.0, 1.0, \dots, 1.0]^T$. A system is considered unstable if any node's value exceeds $10^6$ in absolute value within 1000 steps.
4. Exit with status code `0` if the configuration is stable (Clean).
5. Exit with status code `1` if the configuration is unstable (Evil).

Compile your program to `/home/user/stability_filter`. 

Ensure your C program is highly efficient and handles arbitrary $N \le 100$. Your filter will be rigorously tested against the clean and evil corpora.