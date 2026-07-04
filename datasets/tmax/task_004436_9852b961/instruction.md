You are acting as a bioinformatics analyst. We are studying continuous-time sequence evolution over a k-mer similarity graph to identify stable genetic motifs. We have a custom Rust tool that models this as a continuous-time random walk over the graph using an ordinary differential equation (ODE), reading graph data from HDF5 and integrating the state vector over time.

Unfortunately, our vendored tool at `/app/bio_spectral_graph` is currently failing. The tool uses a custom adaptive Runge-Kutta integrator for the ODE solver. However, it currently diverges (producing NaNs or infinities) on our dataset because the adaptive step-size calculation is inverted—it actually *increases* the step size when the local error is large, immediately violating the stability region. 

Your tasks are:
1. Locate the ODE integrator in the Rust package at `/app/bio_spectral_graph`.
2. Fix the adaptive step size logic. The new step size `dt_next` should be calculated as `dt * (tolerance / error)^0.2`. Currently, it incorrectly calculates `dt * (error / tolerance)^0.2` or similar.
3. Build the corrected Rust package in release mode.
4. Run the compiled executable on our dataset located at `/home/user/data/evolution_graph.h5`. The tool takes the input file path as the first argument and the output file path as the second argument.
5. Save the tool's output to `/home/user/results/state_distribution.csv`.

The output will be a CSV file with two columns: `node_id` and `probability`. Do not modify the output formatting logic of the tool; just fix the integrator and run it. Ensure the output directory exists before running the tool.