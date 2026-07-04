You are a data scientist analyzing astronomical spectroscopy data to find the parameters of an emission line. 

You have been given a raw observational dataset at `/home/user/raw_spectra.txt` and a Go program `/home/user/mcmc_fitter.go` which uses Markov Chain Monte Carlo (MCMC) to estimate the posterior distribution of a Gaussian peak model.

Your task consists of three parts:

1. **Observational Data Reshaping**: 
   The file `/home/user/raw_spectra.txt` is pipe-separated (`|`) and contains three columns: `ObservationID`, `Wavelength`, and `Intensity`. It contains a header and some invalid data rows where `Intensity` is negative or "NaN".
   Use standard Linux command-line tools to filter out the header and any rows where `Intensity` is less than or equal to 0, or is not a valid number. Extract only the `Wavelength` and `Intensity` columns and save them as a comma-separated file at `/home/user/clean_spectra.csv` (e.g., `500.5,12.3`).

2. **Scientific Software Compilation**:
   Compile the MCMC sampling program written in Go. Output the executable to `/home/user/fitter`.

3. **MCMC Sampling & Formatting**:
   Run the compiled executable on your cleaned dataset: `./fitter /home/user/clean_spectra.csv`. 
   The program will output the final posterior mean estimates for four parameters: `Amplitude`, `Center`, `Width`, and `Background` to standard output.
   Capture these final estimates and write them to a log file at `/home/user/final_parameters.log`. The file must contain exactly four lines in this format:
   ```
   Amplitude: <value>
   Center: <value>
   Width: <value>
   Background: <value>
   ```
   (Replace `<value>` with the exact numbers printed by the Go tool).