You are a data scientist analyzing the dynamics of a damped magnetic pendulum from high-speed camera footage. Our laboratory pipeline involves tracking the pendulum's motion, filtering out camera sensor glitches, and fitting a theoretical model to extract the damping coefficient. 

Your objective is to complete the four pipeline stages below. 

**Stage 1: Scientific Software Compilation**
Our custom Mean Squared Error (MSE) evaluator, written in C for performance, needs to be compiled. 
- Source file: `/home/user/src/fast_mse.c`
- Compile this into a shared library `/home/user/src/fast_mse.so` that can be loaded via Python's `ctypes`. The C function signature is `double compute_mse(double* arr1, double* arr2, int length)`.

**Stage 2: Adversarial Corpus Filtering (Sensor Glitch Detection)**
Our camera occasionally drops frames or writes interlacing artifacts, resulting in non-physical "jumps" in tracked trajectories. 
- You are provided a training dataset of trajectory chunks (each containing 20 frames of X,Y coordinates in CSV format) at `/app/corpus/clean/` (valid physics) and `/app/corpus/evil/` (containing sensor glitches).
- Create a Python script `/home/user/glitch_filter.py` that takes a directory path as a command-line argument.
- The script must iterate over all `.csv` files in the given directory and print a line for each file in the format: `<filename>: CLEAN` or `<filename>: EVIL`.
- *Hint:* Clean physical trajectories obey continuous momentum constraints, while "evil" glitches exhibit instantaneous coordinate teleportation (velocity spikes). Your script must strictly identify 100% of glitches while preserving 100% of clean data.

**Stage 3: Video Observational Data Extraction & Reshaping**
- We have captured a new experimental run: `/app/video/experiment_run.mp4`.
- Write a Python script `/home/user/track_pendulum.py` that extracts frames from this video.
- Track the centroid (center of mass) of the pendulum bob (which is the darkest contiguous circular blob in the image).
- Save the reshaped trajectory into `/home/user/observational_data.csv` with columns `frame_index, x, y`. 

**Stage 4: Model Fitting and Convergence Testing**
- The pendulum's X-coordinate motion follows the theoretical damped oscillator model: `x(t) = A * cos(omega * t + phi) * exp(-gamma * t) + C`, where `t` is the `frame_index`.
- Write a Python script `/home/user/fit_model.py` that loads `/home/user/observational_data.csv`.
- Implement a fitting loop that uses the compiled `fast_mse.so` to compute the loss between the observational data and the model predictions. 
- Implement **convergence testing**: Your optimization loop must iteratively update parameters and stop ONLY when the relative change in MSE between successive iterations is less than `1e-6`.
- Save the final fitted parameters into `/home/user/model_params.json` with keys `"A", "omega", "phi", "gamma", "C"`.

Ensure all files are saved in the exact locations specified. We will verify your work by running your filter against a hold-out dataset, checking the video tracking output, and evaluating the final fitted damping coefficient.