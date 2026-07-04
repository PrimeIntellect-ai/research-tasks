You are a performance engineer profiling a molecular network simulation. We've noticed that the simulation produces slightly non-reproducible results across identical runs due to parallel floating-point reduction order variations in the graph algorithm's energy accumulation phase. 

Your task is to quantify this variance by compiling the simulation, collecting a large sample of runs, and orchestrating a notebook-based workflow to calculate the bootstrap confidence interval of the mean energy.

Follow these steps exactly:

1. **Compile the Simulation**:
   A C++ source file is located at `/home/user/sim/network_sim.cpp`. 
   Compile it using `g++` into an executable named `/home/user/sim/run_sim`. Standard C++11 is sufficient.

2. **Collect Data**:
   Write and execute a bash loop in the terminal to run `/home/user/sim/run_sim` exactly 500 times.
   The executable outputs a single floating-point number (the total network energy) to standard output. 
   Redirect and append the output of all 500 runs to a file named `/home/user/data/results.txt`. (Ensure the `/home/user/data` directory exists).

3. **Orchestrate the Analysis**:
   There is a pre-written Jupyter notebook at `/home/user/analysis/bootstrap_ci.ipynb`. This notebook is designed to read `/home/user/data/results.txt`, compute the 95% bootstrap confidence interval of the mean, and write the result to `/home/user/data/final_ci.json`.
   Use `jupyter nbconvert` to execute this notebook from the command line. Save the executed notebook as `/home/user/analysis/bootstrap_ci_executed.ipynb`.

Ensure all output files (`results.txt`, `final_ci.json`, and `bootstrap_ci_executed.ipynb`) exist and are populated correctly by the end of your workflow.