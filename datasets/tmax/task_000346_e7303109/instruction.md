You are a data scientist working on fitting models to experimental trajectory data of a nonlinear oscillator. Some of the data you have collected has been corrupted by a numerical integrator that diverges due to wrong step-size adaptation in the sensor's internal pre-processing. Your task is to build a robust data filter.

**Step 1: Extract Model Parameters**
You have been given a scanned lab note containing the true system parameters. Inspect the image located at `/app/parameters.png` (using OCR tools like `tesseract` which are available on your system). You need to extract three key values: `GAMMA`, `OMEGA`, and `DIVERGENCE_THRESHOLD`.

**Step 2: Compile the Core Library**
Your lab has provided a custom C-based Monte Carlo trajectory generator, but it needs to be compiled. Navigate to `/app/src/` and compile `rk4_core.c` into a shared object file named `librk4.so` using `gcc` with standard shared library flags. 

**Step 3: Build the Trajectory Detector**
Write a Python script at `/home/user/detector.py` that acts as a filter for `.npy` trajectory files.
Your script must accept a single command-line argument: the full path to a `.npy` file.

Each `.npy` file contains a 2D numpy array of shape `(N, 3)`, where the columns correspond to `[time, position, velocity]`. 

For the trajectory in the given file, use multi-dimensional array manipulation to calculate the instantaneous mechanical energy of the system at each time step using the parameters extracted in Step 1:
`Energy = 0.5 * (velocity^2) + 0.5 * (OMEGA^2) * (position^2)`

A trajectory is considered corrupted (diverged due to bad step-size) if its maximum Energy at any point strictly exceeds the `DIVERGENCE_THRESHOLD`. 

Your script `/home/user/detector.py` must:
- Exit with code `0` (Success) if the trajectory is CLEAN (max energy <= threshold).
- Exit with code `1` (Error) if the trajectory is EVIL / DIVERGED (max energy > threshold).

Ensure your script is robust and correctly implements the filtering logic.