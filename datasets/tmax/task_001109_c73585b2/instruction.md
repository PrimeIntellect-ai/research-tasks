You are a data scientist working on a thermal network simulation. We have a Python script that models heat diffusion across a 1D molecular chain represented as a graph. However, the numerical integrator is diverging due to a bug in the adaptive step-size logic, and the spatial resolution of the graph is too coarse. 

You need to perform the following steps to fix the model, refine the domain, and visualize the output.

1. **Fix the Integrator Bug**: 
   The file `/home/user/simulate.py` contains a custom adaptive Forward Euler integrator (`adaptive_integrate`). It estimates the local truncation error by comparing one full step `dt` with two half steps of `dt/2`. If the error exceeds the tolerance, it is supposed to reduce the step size. However, the simulation currently blows up and diverges. Find and fix the logic error in the step-size adaptation.

2. **Implement Mesh Refinement**:
   In the same file, complete the `refine_mesh(nodes, edges, initial_temps)` function. 
   - For every existing edge `[u, v]` in the graph, you must insert exactly one new midpoint node.
   - The new node's ID should be the next available integer (starting from `max(nodes) + 1`).
   - The original edge `[u, v]` should be removed and replaced with two new edges `[u, new_node]` and `[new_node, v]`.
   - The initial temperature of the new midpoint node should be the exact average of the initial temperatures of nodes `u` and `v`.
   - Ensure the function returns the updated `nodes`, `edges`, and `initial_temps`.

3. **Run the Convergence Test**:
   Execute the simulation using the provided `/home/user/graph.json` as input. The script is configured to simulate up to $T = 0.5$ seconds. Ensure the simulation completes successfully without throwing an OverflowError.

4. **Export and Visualize**:
   Modify the bottom of `/home/user/simulate.py` to:
   - Save the final computed temperatures as a JSON object (mapping node IDs as strings to their float temperatures) to `/home/user/final_temperatures.json`.
   - Generate a simple plot of Node ID vs Final Temperature and save it to `/home/user/thermal_plot.png`.

**Constraints and Notes**:
- Use standard Python libraries (`json`, `math`) and `matplotlib` for plotting.
- The `alpha` (thermal diffusivity) is 0.5.
- Do not change the integration method itself, only the adaptive step-size logic.