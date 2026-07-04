I am running a numerical simulation pipeline in a Jupyter Notebook, but I'm encountering a reproducibility issue. Even though I strictly set the random seed in the notebook, the final computed energy of the system fluctuates slightly at the 10th decimal place on every run. 

I've traced the issue to my custom C extension, `sim_core`, which computes the energy. It appears to be suffering from floating-point non-determinism due to the order of reduction operations.

Here is the setup in `/home/user`:
- `/home/user/sim_core.c`: The C source code for the extension.
- `/home/user/setup.py`: The build script for the extension.
- `/home/user/simulation.ipynb`: The notebook that generates the system state, calls `sim_core.compute_energy`, and prints the final energy.

Please do the following:
1. Identify and fix the floating-point reduction order issue in `/home/user/sim_core.c`. You should prioritize strict mathematical determinism (sequential left-to-right summation is fine, even if it means sacrificing OpenMP parallelization).
2. Recompile and install the `sim_core` extension into the current Python environment.
3. Execute the notebook `/home/user/simulation.ipynb` programmatically (e.g., using `jupyter nbconvert --execute` or `papermill`).
4. Extract the newly deterministic final energy value printed by the notebook and save it to a file named `/home/user/reproducible_energy.txt`. The file should contain only the numerical value.

Ensure that running the notebook multiple times produces exactly the same floating-point value.