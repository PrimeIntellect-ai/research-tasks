You are a data scientist tasked with fitting a network diffusion model to experimental data. 

You have been provided a baseline C program at `/home/user/network_diffusion.c` that simulates heat diffusion over a 4-node line graph. The system is modeled as $dx/dt = -\beta L x$, where $L$ is the graph Laplacian, and $x$ is the state vector. 

Currently, the C program uses an explicit Euler integration scheme, but it diverges (produces NaNs or infinities) because the hardcoded time step (`dt`) is too large for the integration to be stable.

Your tasks are:
1. **Fix the Integrator**: Modify `/home/user/network_diffusion.c` to use a stable time step of `dt = 0.01`. The total simulation time `T` should remain `5.0`.
2. **Implement Distance Metric**: Add a function to the C program to compute the Kullback-Leibler (KL) divergence between the simulated distribution at time `T` and the experimental distribution. Treat the state vector $x$ as a probability distribution (it sums to 1.0). The KL divergence formula is $D_{KL}(P || Q) = \sum P_i \log(P_i / Q_i)$, where $P$ is the experimental data and $Q$ is the simulated data.
3. **Model Fitting**: Implement a search routine within the C program to find the optimal diffusion rate $\beta$ that minimizes the KL divergence between the simulation and the experimental data. 
   - Search the space of $\beta$ from `0.10` to `1.00` in increments of `0.01`.
   - The experimental data at $T=5.0$ is: `x[0]=0.370, x[1]=0.286, x[2]=0.205, x[3]=0.139`.
4. **Save Results**: Output the optimal $\beta$ (formatted to two decimal places, e.g., `0.55`) to `/home/user/result.txt`.
5. **Visualization**: Write a Python script to plot a grouped bar chart comparing the experimental distribution and the simulated distribution at the optimal $\beta$. Save the plot to `/home/user/plot.png`.

Ensure all files are created in `/home/user/`. You will need to compile and run your modified C code.