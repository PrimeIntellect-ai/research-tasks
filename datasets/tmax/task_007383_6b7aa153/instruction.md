You are an AI assistant helping a machine learning engineer prepare training data based on molecular thermal profiles. 

I have a Python script at `/home/user/heat_sim.py` that is supposed to:
1. Parse a PDB file (`/home/user/input.pdb`) to extract the 3D coordinates (X, Y, Z) of all `ATOM` records.
2. Map these atoms onto a uniform 3D cubic mesh (domain decomposition) spanning from -10.0 to 10.0 in X, Y, and Z dimensions, with exactly 20 grid points in each dimension (i.e., a 20x20x20 grid). Each grid cell containing at least one atom starts with a temperature of 100.0, while all other cells start at 0.0.
3. Simulate heat diffusion on this mesh using an explicit finite difference method for 500 time steps. The thermal diffusivity constant `alpha` is set to `0.1`.
4. Plot the maximum temperature of each Z-slice at the final time step and save it to `/home/user/z_profile.png`.
5. Save the global maximum temperature at the final time step to `/home/user/max_temp.txt` (just the floating point number).

However, the current script produces `NaN` or infinite values because the numerical integration diverges. The explicit Euler step size (`dt`) in the script is hardcoded to `0.5`, which violates the Courant-Friedrichs-Lewy (CFL) stability condition for 3D diffusion (`dt <= dx^2 / (6 * alpha)`).

Your task:
1. Fix the numerical stability issue in `/home/user/heat_sim.py` by calculating and using the maximum stable time step `dt` according to the 3D diffusion stability condition.
2. Run the fixed script to process `/home/user/input.pdb`.
3. Ensure `/home/user/z_profile.png` is generated successfully.
4. Ensure `/home/user/max_temp.txt` contains the correct final maximum temperature (rounded to 4 decimal places).

The provided files are already in `/home/user/`. You can install any standard Python scientific libraries you need (like `numpy`, `matplotlib`).