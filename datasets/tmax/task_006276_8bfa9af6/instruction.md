You are an AI assistant acting as a Machine Learning Engineer. You need to prepare synthetic spectroscopy data for a neural network that predicts molecular vibration modes from simulated sensor data.

We are modeling a simplified molecule as a network of coupled oscillators (masses and springs). You must write a Go program that simulates this system, extracts the time-domain signal, processes it into a frequency-domain power spectrum, and identifies the dominant vibration frequency.

Here are the precise specifications:

1. **System Definition**: 
   A file at `/home/user/molecule.txt` contains the system configuration.
   The first line contains space-separated masses for $N$ nodes.
   The following $N$ lines contain an $N \times N$ adjacency matrix representing the spring constants $k_{ij}$ between nodes $i$ and $j$.
   (Assume $k_{ii} = 0$).

2. **Simulation (ODE Solving)**:
   Write a Go program in `/home/user/synth_data/main.go` (you should initialize a Go module here).
   The program must simulate the system using the Symplectic Euler method:
   For each time step:
   a. Compute accelerations: $a_i = \frac{1}{m_i} \sum_{j} k_{ij} (x_j - x_i)$
   b. Update velocities: $v_i(t+dt) = v_i(t) + a_i \times dt$
   c. Update positions: $x_i(t+dt) = x_i(t) + v_i(t+dt) \times dt$
   
   - Total steps: $1024$
   - Time step ($dt$): $0.01$ seconds
   - Initial conditions: $x_0 = 1.0$, all other $x_i = 0.0$. All $v_i = 0.0$.

3. **Signal Processing**:
   - Extract the position time-series of **Node 0** ($x_0(t)$) over the 1024 steps.
   - Compute the Discrete Fourier Transform (DFT or FFT) of this 1024-point real sequence.
   - Calculate the magnitude of each complex frequency component.

4. **Spectroscopy Output**:
   - Identify the frequency (in Hz) of the maximum magnitude peak. **Ignore the DC component (0 Hz)**.
   - The frequency of index $k$ is given by $f_k = \frac{k}{N \cdot dt}$.
   - Write ONLY the dominant frequency in Hz (formatted to 4 decimal places, e.g., `2.2461`) to `/home/user/peak.txt`.

You must execute the Go program so that `/home/user/peak.txt` is generated successfully.