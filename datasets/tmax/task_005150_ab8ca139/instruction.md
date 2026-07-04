You are a Machine Learning Engineer preparing a dataset to train a Physics-Informed Neural Network (PINN). The training data must consist of highly accurate trajectories of a dynamic physical system.

Your colleague provided an image of the system specifications, located at `/app/equation_params.png`. This image contains the name of the system (a well-known oscillator), the stiffness parameter (`mu`), the initial conditions, the integration time span, and the required number of output points. 

Your colleague also provided a draft script at `/home/user/generate_data.py`. Unfortunately, this script produces "NaN" values or wildly diverging trajectories because the physical system is highly stiff, and the default numerical integrator uses incorrect step-size adaptation.

Your task is to:
1. Extract the physical parameters, initial conditions, time span, and required number of time steps from `/app/equation_params.png`. You may use OCR tools like `tesseract` or basic vision processing.
2. Fix the `/home/user/generate_data.py` script. You must switch to a numerical solver appropriate for stiff Ordinary Differential Equations (ODEs) and perform convergence testing to ensure your integration tolerances are tight enough to avoid divergence. Validate that your numerical solution correctly captures the rapid transitions characteristic of this system.
3. Reshape the observational data into a specific ML-ready format. The final output must be saved to `/home/user/training_data.csv`. The CSV must have exactly three columns in this order: `t` (time), `y1` (position), and `y2` (velocity/momentum). It must contain exactly the number of evenly spaced points requested in the image (including the start and end times).
4. Generate a phase portrait visualization of the experimental data (plotting `y2` vs `y1`) and save it to `/home/user/phase_portrait.png` to visually validate the limit cycle.

Ensure the final dataset in `/home/user/training_data.csv` is highly accurate. An automated grader will compare your CSV against a high-precision reference numerical solution.