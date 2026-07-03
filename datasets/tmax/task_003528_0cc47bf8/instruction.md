You are assisting a computational physics researcher who has been running numerous non-linear root-finding simulations. The simulations use an adaptive-step integrator to find the steady states of a specific non-linear system. Unfortunately, the step-size adaptation occasionally fails, causing the trajectories to diverge or get stuck in non-physical limit cycles.

The researcher has saved the trajectories of these simulations as HDF5 files. Each HDF5 file contains two datasets: `x` and `y`, representing the time-series arrays of the simulation.

Your task is to build an automated filter to separate the converged (clean) simulations from the diverged/stuck (evil) simulations. 

Here are your instructions:
1. Setup your Python environment. You will need libraries to read HDF5 files and process images.
2. The definition of the non-linear system and the required convergence tolerance are locked in an image file located at `/app/system_def.png`. You must use OCR (e.g., `pytesseract` and `Pillow`, tesseract is available on the system) to extract the equations and the tolerance threshold.
3. Write a Python CLI script at `/home/user/check_convergence.py` that takes a single argument (the path to an HDF5 file).
4. The script must read the final values of the `x` and `y` arrays from the HDF5 file.
5. The script must evaluate the equations extracted from the image at this final state.
6. If the final state is a valid root of the system (both equations evaluate to 0 within the OCR'd tolerance), the script must exit with status code `0` (accept).
7. If the final state violates the tolerance (diverged, NaN, or stuck in a local minimum), the script must exit with status code `1` (reject).

The script must be robust enough to handle NaNs and extreme values without crashing (it should cleanly exit with `1` in these cases).

To test your script, the researcher has provided a subset of files in:
- `/app/corpora/clean/` (all these should exit `0`)
- `/app/corpora/evil/` (all these should exit `1`)

Ensure your classifier script works flawlessly on these datasets, as it will be evaluated against a hidden verification set with the exact same properties.