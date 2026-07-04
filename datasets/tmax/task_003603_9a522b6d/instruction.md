You are a bioinformatics analyst tasked with analyzing circadian rhythm gene expression data. 
You have been provided with a raw, noisy dataset containing time-series expression levels for several key clock genes. The data is currently in a disorganized JSON format.

Your objective is to reshape this data, identify the dominant periodicities using spectral analysis, and refine these periods using curve fitting optimization.

Here are the detailed steps:

1. **Setup**:
   The raw data is located at `/home/user/data/raw_expression.json`. 
   It contains a list of records. Each record has `gene_id`, `time_hours`, and `expression_level`. The data is scrambled and not sorted by time.

2. **Data Reshaping**:
   Write a Python script at `/home/user/analyze.py` to parse the JSON and reshape it into a structured format (e.g., a Pandas DataFrame) where you can access the time-series expression data for each distinct `gene_id` sorted chronologically by `time_hours`.

3. **Spectral Analysis (Initial Guess)**:
   For each gene, use a Fast Fourier Transform (FFT) on the sorted expression levels to estimate the dominant frequency. Convert this frequency to the dominant period (in hours). Use this dominant period as the initial guess ($T_{guess}$) for the optimization step.

4. **Curve Fitting (Optimization)**:
   Fit the following trigonometric model to the expression data of each gene using nonlinear least squares optimization (e.g., `scipy.optimize.curve_fit`):
   $$y(t) = A \cdot \cos\left(\frac{2 \pi}{T} t + \phi \right) + B$$
   Where:
   - $t$ is `time_hours`
   - $A$ is the amplitude
   - $T$ is the period (initialized with $T_{guess}$)
   - $\phi$ is the phase shift
   - $B$ is the baseline expression level
   
   *Constraints for standardization*: 
   Ensure that your final fitted parameters satisfy $A > 0$ and $0 \le \phi < 2\pi$. If your optimizer yields a negative $A$, multiply $A$ by -1 and add $\pi$ to $\phi$. Finally, take $\phi \pmod{2\pi}$.

5. **Output Results**:
   Your script must generate a CSV file at `/home/user/results/gene_fits.csv` with the following exact columns:
   `gene_id,amplitude,period,phase,baseline`
   
   The rows must be sorted alphabetically by `gene_id`.
   Round all numerical values to exactly 3 decimal places.

*Note*: You may need to install necessary Python packages like `pandas`, `numpy`, and `scipy`. You can run your script and verify the output. Once `/home/user/results/gene_fits.csv` is correctly populated, your task is complete.