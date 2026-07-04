You are a bioinformatics analyst working on modeling mRNA decay from time-series sequencing data. You have received an export of RNA read counts over time, but it is in a poorly formatted text file. 

The known biological model for the transcript concentration $C(t)$ follows the Ordinary Differential Equation (ODE):
$$ \frac{dC}{dt} = \alpha - \beta C $$
Where $\alpha$ is the basal transcription rate and $\beta$ is the decay rate constant.
For this specific transcript, experiments have determined that $\alpha = 10.0$ and $\beta = 5.0$. The initial concentration at $t=0$ is $C(0) = 100.0$.

Your task is to complete the following steps:

1. **Data Reshaping**: 
   Read the raw observational data located at `/home/user/rna_data.txt`. The data alternates between time point identifiers and read counts. Parse this file and reshape it into a clean, comma-separated values file at `/home/user/observed_data.csv` with exactly two columns: `time` (float) and `count` (float). 

2. **Numerical Integration and Analytical Validation**:
   Write a Python script `/home/user/simulate.py` that:
   - Calculates the **analytical solution** for the transcript concentration at exactly $t = 1.0$.
   - Calculates the **numerical solution** for the transcript concentration at exactly $t = 1.0$ using the **explicit (forward) Euler method** with a time step of $\Delta t = 0.1$.
   
3. **Numerical Stability Testing**:
   - Determine the theoretical **maximum stable time step** ($\Delta t_{max}$) for the explicit Euler method for this specific ODE. This is the supremum time step before the numerical solution strictly diverges or oscillates with strictly increasing amplitude.

4. **Output Generation**:
   Your script `/home/user/simulate.py` must execute and save its results to a JSON file located at `/home/user/results.json`. The JSON file must have exactly the following keys and structure:
   ```json
   {
       "analytical_t_1": <float>,
       "numerical_t_1": <float>,
       "max_stable_dt": <float>
   }
   ```
   (Round all floats to 5 decimal places).

Ensure all code runs successfully in the default Python environment.