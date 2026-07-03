Hello! I am a researcher working on simulating an epidemic spread on a contact network using a discrete-time SIR (Susceptible-Infected-Recovered) model. 

I've been trying to calibrate the model parameters ($\beta$ for infection rate, $\gamma$ for recovery rate) using an MCMC sampling approach, but my numerical integrator keeps diverging or producing unphysical values (like negative populations) because my time-step adaptation is wrong. 

A colleague sent me a screenshot of the correct adaptive time-step rule for this specific model, but it is saved as an image at `/app/step_rule.png`. I need you to extract this formula and implement the full MCMC evaluation script.

Here is what you need to do:
1. Use OCR (e.g., `tesseract`) to read the formula from `/app/step_rule.png`. It contains a simple arithmetic formula for the step size `h` based on `beta` and `gamma`.
2. Write a Python script at `/home/user/sim_mcmc.py` that evaluates MCMC proposals. 
3. The script must read from `stdin`. 
   - The first line contains an integer `N` (number of nodes).
   - The next line contains an integer `E` (number of edges).
   - The next `E` lines contain two space-separated integers `u v` representing an undirected edge between node `u` and node `v`.
   - After the edges, the string `---` appears on its own line.
   - The remaining lines contain pairs of space-separated floats representing proposed MCMC parameters: `beta` and `gamma`.
4. For EACH proposed `beta` and `gamma` pair, run a deterministic simulation:
   - Initial state: Node 0 is Infected ($I_0 = 1.0$), all other $N-1$ nodes are Susceptible ($S_i = 1.0$). All Recovered $R_i = 0.0$.
   - Simulate for exactly 50 steps.
   - For each step, compute the adaptive step size `h` using the extracted formula. 
   - Update the state for all nodes simultaneously using the discrete Euler rule:
     $S_i^{(new)} = S_i - h \cdot \beta \cdot S_i \cdot \sum_{j \in Neighbors(i)} I_j$
     $I_i^{(new)} = I_i + h \cdot \beta \cdot S_i \cdot \sum_{j \in Neighbors(i)} I_j - h \cdot \gamma \cdot I_i$
     $R_i^{(new)} = R_i + h \cdot \gamma \cdot I_i$
   - If any node's $S, I,$ or $R$ drops below 0.0 during the 50 steps, the simulation for this proposal immediately fails (reject).
   - Otherwise, calculate the total final infected population $I_{total} = \sum_{i=0}^{N-1} I_i$.
   - The MCMC proposal is "accepted" if $0.5 < I_{total} < 5.0$, and "rejected" otherwise.
5. For each proposal, print `1` if accepted, or `0` if rejected, each on a new line to `stdout`.

Please ensure your simulation is deterministic, uses basic Python `float` arithmetic, and strictly follows the Euler update order (compute all derivatives based on the current state, then apply updates).