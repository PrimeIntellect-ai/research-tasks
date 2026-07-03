I need you to help me debug and complete a simulation analysis pipeline. I am running a simulation of a reaction-diffusion process on a molecular graph network. The initial state of the network was encoded into an audio file by a previous intern, and the numerical integration script they left behind keeps diverging and producing `NaN`s because the step-size adaptation logic is broken.

Here is what you need to do:

1. **Environment Setup**: Create a Python virtual environment at `/home/user/sim_env` and install `numpy`, `scipy`, `networkx`, and `soundfile` or `librosa` to process the audio.
2. **Audio Decoding**: Read the audio file located at `/app/init_state.wav`. The audio contains 10 interleaved channels, each representing the initial state value for a node in a 10-node cycle graph. Extract the first sample of each channel. These 10 values are the initial concentrations $C_i(0)$ for nodes $i \in \{0, 1, \dots, 9\}$.
3. **Graph Setup**: Create a cycle graph (ring network) of 10 nodes. The Laplacian matrix $L$ of this graph will drive diffusion.
4. **Numerical Integration**: The system is governed by the ODE: 
   $\frac{dC}{dt} = -k \cdot L \cdot C + \alpha \cdot C \cdot (1 - C)$
   where $k = 0.5$ (diffusion rate) and $\alpha = 0.1$ (reaction rate).
   The intern's code used a custom Runge-Kutta 4 integrator with adaptive step size, but the step size grows too fast and diverges. Write a script that integrates this system from $t=0$ to $t=10.0$.
   Instead of using their broken logic, you must implement a simple adaptive step size: start with $dt = 0.1$. After each step, if the maximum absolute change in any node's concentration exceeds $0.05$, halve the step size and recompute the step. If the max change is less than $0.01$, double the step size for the next step. Ensure $dt$ is capped at a maximum of $0.1$ and a minimum of $0.001$.
5. **Metric Output**: After reaching $t=10.0$, compute the mean concentration across all 10 nodes. Write this single floating-point number to `/home/user/final_mean.txt`.

Please write the complete Python script to `/home/user/run_sim.py` and run it to produce `/home/user/final_mean.txt`.