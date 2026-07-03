You are a machine learning engineer preparing biochemical time-series training data for a neural network. You need to simulate a system of ordinary differential equations (ODEs) using initial conditions derived from protein sequences, test the numerical stability of a basic solver, and export the high-fidelity data to an HDF5 file.

Follow these steps exactly:

1. **Parse Initial Conditions from FASTA:**
   Read the file `/home/user/input.fasta`. It contains 5 protein sequences. Calculate the estimated molecular weight of each sequence by multiplying the number of amino acids (characters) in the sequence by `110.0` Da. Use these 5 weights as the initial conditions $y_1(0)$ to $y_5(0)$ for your ODE system, preserving the order of the sequences in the file.

2. **Simulate the ODE System:**
   The biochemical process is modeled by the following coupled ODEs for $i \in \{1, 2, 3, 4, 5\}$:
   $$ \frac{dy_i}{dt} = -0.1 y_i + 0.01 \sum_{j \neq i} y_j $$
   Use a high-quality numerical solver (like `scipy.integrate.odeint` or `solve_ivp`) to solve this system from $t = 0$ to $t = 100$. Evaluate the solution at exactly 1000 evenly spaced time points (starting at 0 and ending at 100).

3. **Export Training Data:**
   Save the high-fidelity trajectory data (a 1000x5 numerical array) into an HDF5 file located at `/home/user/training_data.h5`. Create a dataset inside this file named `simulated_trajectories` to store the array.

4. **Numerical Stability Test & Visualization:**
   To justify using the high-quality solver, demonstrate the instability of the forward Euler method on this stiff-like system. Implement the forward Euler method manually: $y(t+dt) = y(t) + dt \cdot f(y(t))$.
   Solve the exact same ODE system from $t = 0$ to $t = 100$ using the forward Euler method with a large step size of $dt = 25.0$. 
   Plot the trajectory of the first component ($y_1$) over time from the Euler simulation. Save this plot as `/home/user/stability_plot.png`.

Ensure all output files (`/home/user/training_data.h5` and `/home/user/stability_plot.png`) are created accurately.