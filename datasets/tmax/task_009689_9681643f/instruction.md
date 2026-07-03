You are an AI assistant helping a physics researcher automate their simulation data analysis. The researcher has a set of noisy output logs from a spring-mass harmonic oscillator simulation, but the data is messy, and the simulation software didn't calculate the spring stiffness constant ($k$).

Your objective is to build a Bash-based data processing pipeline and a regression testing suite to extract $k$ and verify the calculations. 

**Background Physics:**
The dominant frequency $f$ (in Hz) of a spring-mass system is given by $f = \frac{1}{2\pi} \sqrt{\frac{k}{m}}$, where $m$ is the mass in kg. Therefore, $k = m (2\pi f)^2$.

**Directory Structure:**
- Raw data is in `/home/user/sim_data/` (contains files like `exp_1.log`, `exp_2.log`).
- Reference values for regression tests are in `/home/user/sim_data/reference.csv`.
- You must create the directory `/home/user/plots/` for visual outputs.

**Task Requirements:**

1. **Write the Analysis Script (`/home/user/process.sh`):**
   - Write a Bash script that takes a single log file path as its first argument.
   - The script must parse the mass ($m$) from the header of the log file.
   - It must reshape the messy time-series data (format: `t=<time>, val=<amplitude>`) into a clean format to perform a Fourier Transform (FFT). You may use Python (via `python3 -c` or a temporary script invoked by the Bash script) to perform the FFT to find the dominant frequency $f$.
   - Calculate the spring stiffness $k$ using the formula above.
   - Generate a frequency spectrum plot of the data and save it to `/home/user/plots/<filename_without_ext>_spectrum.png` (e.g., `exp_1_spectrum.png`). You can install and use Python packages like `numpy` and `matplotlib` in user space (`pip install --user`) if needed.
   - The script must print *only* the calculated $k$ value to standard output, rounded to 2 decimal places.

2. **Write the Regression Test Suite (`/home/user/run_tests.sh`):**
   - Write a Bash script that iterates over all `exp_*.log` files in `/home/user/sim_data/`.
   - For each file, it should execute `./process.sh`.
   - Compare the outputted $k$ value against the expected value in `/home/user/sim_data/reference.csv`. An absolute difference of $\le 5.0$ is considered a `PASS`.
   - The test suite must output a report to `/home/user/regression_report.txt` in the exact following format for each file:
     `[PASS|FAIL] <filename>: Expected <ref_k>, Got <calc_k>`

**Data Format Details:**
The log files (`/home/user/sim_data/exp_*.log`) have the following format:
```
Simulation ID: <id>
Mass (kg): <mass>
-- DATA START --
t=0.000, val=0.123
t=0.010, val=0.456
...
```

The reference file (`/home/user/sim_data/reference.csv`) format is:
```
exp_1.log,315.83
exp_2.log,725.71
```

Set up the scripts, ensure they are executable (`chmod +x`), and run `/home/user/run_tests.sh` so that the `regression_report.txt` and the PNG plots are generated.