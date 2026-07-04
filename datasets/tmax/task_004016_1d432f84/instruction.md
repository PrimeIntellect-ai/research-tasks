You are an AI assistant helping a researcher optimize a simulation model. 

The researcher has collected some raw observational data from a physics experiment, but it requires preprocessing, and they need to find the correct parameters for a legacy simulator to match this data.

Here are your steps to complete the task:

1. **Compile Preprocessing Tool**: 
   You have been provided with the source code for a data denoising tool in C at `/app/src/denoise.c`. Compile it into an executable at `/home/user/denoise` using `gcc` (with standard math library linked, `-lm`).

2. **Data Reshaping**: 
   The raw observational data is located at `/home/user/raw_data.json`. It is a list of JSON objects, each containing a timestamp `time` and an array of noisy sensor readings `sensors`. Write a Python script to reshape this data into a CSV format. For each timestamp, compute the median of the `sensors` array. Save the intermediate result to `/home/user/reshaped.csv` with the header `t,val`.

3. **Denoising**: 
   Run your compiled `denoise` tool on `/home/user/reshaped.csv`. The tool reads from standard input and prints to standard output. Save the denoised output to `/home/user/processed_data.csv`.

4. **Simulation Optimization**:
   There is a legacy simulator at `/app/sim_model` (a stripped binary). It takes exactly three positional float arguments representing physical parameters: `alpha`, `beta`, and `gamma`. 
   For example: `/app/sim_model 1.0 5.0 2.5`
   The simulator outputs a time series in CSV format (`t,sim_val`) to standard output.
   
   Write an optimization script in Python (you may use `scipy.optimize`) that repeatedly calls the `/app/sim_model` binary to find the optimal parameters (`alpha`, `beta`, `gamma`) that minimize the Mean Squared Error (MSE) between the simulated values (`sim_val`) and the `val` column in `/home/user/processed_data.csv` for matching time steps.
   Assume all three parameters are bounded between `0.1` and `15.0`.

5. **Final Output**:
   Once your optimization converges, save the optimal parameters as a single comma-separated line (e.g., `1.234,5.678,9.012`) to the file `/home/user/best_params.txt` in the order `alpha,beta,gamma`.