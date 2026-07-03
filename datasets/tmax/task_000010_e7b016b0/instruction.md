You are an ML engineer preparing a training dataset for a Physics-Informed Neural Network (PINN). The dataset consists of sensor logs (CSV files) tracking a physical system, but the sensors are prone to severe glitches. You need to build a robust filtering pipeline using Bash to isolate the physically valid data.

First, you must calibrate your theoretical model using a provided calibration video:
1. Extract and analyze the frames of the video located at `/app/calibration.mp4`.
2. Count the exact number of completely red frames in this video. This integer count is your calibration parameter `C`.
3. Orchestrate a pre-existing Jupyter notebook (`/app/solve_ode.ipynb`) using `papermill`. This notebook contains a nonlinear ODE solver. You must execute it, passing the parameter `C` to the notebook (the notebook expects a parameter named `C`).
4. Upon successful execution, the notebook will generate a reference ground-truth trajectory file at `/tmp/reference_solution.csv` (format: `time,value`).

Next, implement the dataset filter:
Write a Bash script at `/home/user/sanitize.sh` with the following signature:
`bash /home/user/sanitize.sh <input_dir> <output_dir>`

For every `.csv` file in `<input_dir>`, your script must:
1. Compare its `value` column against the `value` column in `/tmp/reference_solution.csv`.
2. Calculate the Maximum Absolute Error (MAE) between the two trajectories. Both files have identical timestamps and exactly 100 rows.
3. If the maximum absolute difference at any single time step is strictly less than `0.5`, the data is valid. Copy the file to `<output_dir>` with its original filename.
4. If the difference is `0.5` or greater, it is considered anomalous/glitchy and must be rejected (do not copy it).

The automated testing system will invoke your script against a hidden testing dataset containing both clean and corrupted sensor logs. Your script must correctly reject 100% of the corrupted logs and preserve 100% of the clean logs.