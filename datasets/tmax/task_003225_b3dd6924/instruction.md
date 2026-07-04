You are acting as a data scientist analyzing how the genetic composition of different viral strains affects their replication dynamics. 

You have been provided with a FASTA file containing several viral sequences at `/home/user/viral_sequences.fasta`.

Your task is to write and execute a Python script that performs the following workflow:

1. **Parse the Sequence Data:** Read the FASTA file. For each sequence, calculate its GC-content fraction (the count of 'G' and 'C' nucleotides divided by the total sequence length).
2. **Determine Growth Rate:** For each sequence, compute a specific growth rate $r$ using the formula: $r = 0.5 \times (\text{GC-content fraction})$.
3. **Numerical Integration:** Simulate the viral load $V(t)$ for each sequence using the logistic growth ordinary differential equation (ODE):
   $dV/dt = r \cdot V \cdot \left(1 - \frac{V}{K}\right)$
   Use a carrying capacity $K = 1000$ and an initial condition $V(0) = 1.0$. Integrate the ODE over the time span from $t = 0$ to $t = 50$, evaluating at exactly 100 evenly spaced time points (using `numpy.linspace(0, 50, 100)`).
4. **Export to HDF5:** Save the resulting viral load time-series data into an HDF5 file located at `/home/user/viral_simulation.h5`. The root of the HDF5 file must contain datasets named exactly after the sequence IDs from the FASTA file (e.g., if a sequence has the header `>Strain_X`, the dataset should be named `Strain_X`). Each dataset must be a 1D array of 100 float values representing $V(t)$ at the evaluated time points.
5. **Data Visualization:** Generate a line plot showing the viral load $V(t)$ over time for all sequences on a single set of axes. Label the x-axis "Time", the y-axis "Viral Load", and include a legend with the sequence IDs. Save this plot to `/home/user/viral_plot.png`.

You may need to install necessary Python packages (such as `h5py`, `scipy`, `matplotlib`, and `biopython`) using `pip` before writing and running your script.

Ensure your script completes successfully and all output files (`/home/user/viral_simulation.h5` and `/home/user/viral_plot.png`) are generated at the exact specified paths.