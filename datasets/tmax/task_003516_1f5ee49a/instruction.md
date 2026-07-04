You are an AI assistant acting as a bioinformatics analyst. We are studying a synthetic biological system where a specific protein's concentration $y(t)$ is driven by the GC content of a genetic sequence. 

You have been provided with:
1. An image `/app/kinetics.png` containing the reaction kinetics parameters. You will need to extract the production rate ($\alpha$) and degradation rate ($\beta$) from this image.
2. A directory of FASTA sequences containing a mix of valid sequences and harmful "evil" sequences. The "evil" sequences cause the steady-state protein concentration to exceed a safe threshold of `250.0`.

Your goals are:
1. **Parameter Extraction**: Extract $\alpha$ and $\beta$ from `/app/kinetics.png` (using OCR, e.g., `tesseract`).
2. **ODE Solver & Filter in C**: Write a C program at `/home/user/filter.c` and compile it to `/home/user/filter`. 
   - The program must take a FASTA file path as its first CLI argument.
   - It should parse the FASTA file to count the total number of 'G' and 'C' bases ($N_{GC}$) in the sequence lines (ignore headers starting with `>` and newlines, case-insensitive).
   - It must implement a Forward Euler numerical solver for the ODE: 
     $dy/dt = \alpha \cdot N_{GC} - \beta \cdot y$
   - Use a time step $\Delta t = 0.1$ and initial condition $y(0) = 0.0$.
   - Implement convergence testing: stop the simulation when the absolute difference between successive steps $|y(t) - y(t - \Delta t)| < 10^{-5}$.
   - If the converged steady-state value of $y$ is strictly greater than `250.0`, the program must reject the sequence by returning exit code `1` (evil).
   - If the converged value is $\le 250.0$, it must accept the sequence by returning exit code `0` (clean).
3. **Data Visualization**: Run your solver on `/app/sample.fasta` and modify it to output the time-series data $(t, y)$ to `/home/user/timeseries.csv`. Then, use a command-line tool (like `gnuplot` or a simple script) to plot this data, saving the visualization to `/home/user/plot.png`.

We will test your `/home/user/filter` executable against a hidden evaluation corpus to verify it correctly accepts all clean sequences and rejects all evil sequences.