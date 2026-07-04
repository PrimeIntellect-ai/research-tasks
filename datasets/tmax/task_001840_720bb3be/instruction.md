You are an astrobiology researcher analyzing the latest simulation run for an extremophile protein model. Some of your previous simulation analyses produced non-reproducible results due to floating-point reduction order errors when summing large arrays of single-precision measurements.

Your task is to build a robust data processing pipeline that extracts the initial parameters, integrates the fluxes, and computes a bootstrap confidence interval.

Here are the details:
1. **Audio Transcription**: You have an audio recording of the lab notes at `/app/experiment_log.wav`. Listen to/transcribe this audio to extract the cooling rate (a float value). Let's call this $r$.
2. **Bioinformatics Parsing**: You have a protein structure at `/app/molecule.pdb`. Parse this file to count the total number of Carbon atoms (element 'C'). Let's call this $N_C$.
3. **Numerical Integration**: The simulation data is stored in an HDF5 file at `/app/sim_results.h5` under the dataset name `trials`. This dataset contains 100 rows (trials) and 50,000 columns (time steps) of `float32` values. 
   - Perform a numerical integration of each trial over time using the trapezoidal rule. The time step size is $dt = 0.002$. 
   - *Crucial*: Because the data is single-precision (`float32`), a naive sum will accumulate large floating-point errors over 50,000 elements. You must ensure your reduction/summation is done in `float64` precision (or use Kahan summation) to achieve reproducible, high-precision results.
   - Let the integrated value for trial $i$ be $I_i$.
4. **Analytical Validation**: The theoretical expected value for the integral is $E = N_C \times r$. Compute this.
5. **Statistical Analysis**: Using the 100 integration results ($I_1, \dots, I_{100}$), compute the 95% bootstrap confidence interval for the mean. 
   - Use exactly 10,000 bootstrap resamples.
   - Use the standard percentile method.
   - For reproducibility in your script, set the random seed to `42` (if using numpy: `np.random.seed(42)`).

Output your final results into a JSON file at `/home/user/summary.json` with the following structure:
```json
{
  "audio_rate": <float>,
  "carbon_count": <int>,
  "analytical_value": <float>,
  "bootstrap_mean": <float>,
  "bootstrap_lower": <float>,
  "bootstrap_upper": <float>
}
```

Ensure your JSON file is formatted correctly. The evaluation will check the numerical accuracy of your `bootstrap_mean` against a high-precision reference.