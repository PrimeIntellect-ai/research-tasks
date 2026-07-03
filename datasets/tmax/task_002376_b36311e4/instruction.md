I am a researcher studying damped harmonic oscillators, and I need to test the numerical stability of my simulation pipeline across different initial conditions. I have a simulation script and a spectral analysis tool, but I need a reproducible Bash pipeline to automate the validation.

My files are located in `/home/user/sim_env/`:
- `run_sim.sh`: A shell script that takes an integer random seed as an argument (e.g., `./run_sim.sh 1`) and outputs a time-series dataset to `/home/user/sim_env/output.csv`.
- `find_peak.py`: A Python script that reads `output.csv`, performs a Fast Fourier Transform (FFT) to find the dominant frequency, and prints it to standard output. 

Please write a Bash script at `/home/user/validate_stability.sh` that performs the following steps:
1. Creates a Python virtual environment at `/home/user/venv`.
2. Activates the virtual environment and installs `numpy`.
3. Loops through integer random seeds from `1` to `5` (inclusive).
4. For each seed:
   - Runs `./run_sim.sh <seed>`.
   - Runs `find_peak.py` using the virtual environment's Python interpreter to determine the peak frequency of that simulation run.
5. Calculates the average dominant frequency across all 5 runs using standard bash tools (e.g., `awk` or `bc`).
6. Writes the final average to `/home/user/stability_report.txt` in the exact format: `Average Frequency: X.XXX Hz` (rounded to exactly 3 decimal places).

Once you have written `validate_stability.sh`, execute it so that `/home/user/stability_report.txt` is generated and I can review the results.