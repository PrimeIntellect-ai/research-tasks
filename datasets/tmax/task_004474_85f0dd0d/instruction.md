You are an AI assistant acting as a computational researcher. We are modeling a predator-prey system (Lotka-Volterra ODE system) and need to filter out corrupted or non-physical observational data collected from various sensors.

Your objectives:
1. Environment Management: Set up a Python virtual environment at `/home/user/sim_env` and install the necessary scientific computing libraries (`scipy`, `numpy`, `pandas`, `pytesseract`, `pillow`). 
2. Parameter Extraction: We have a scanned image of lab notes located at `/app/lab_notes_scan.png`. Use OCR (tesseract is available on the system) to extract the baseline Lotka-Volterra parameters (`alpha`, `beta`, `delta`, `gamma`).
3. ODE Baseline Simulation: Using the extracted parameters, simulate the system from t=0 to t=50. The initial conditions at t=0 are `prey = 10.0` and `predator = 5.0`.
4. Trace Classification: Write a Python script at `/home/user/trace_filter.py` that processes a directory of observational data and classifies each trace. 

The entry point for your script MUST be exactly:
`python3 /home/user/trace_filter.py --input <input_dir> --output <output_dir>`

Behavior of `trace_filter.py`:
- Read all `.csv` files in the `<input_dir>`. Each file has columns `time`, `prey`, and `predator`.
- The script must reshape and compare this observational data to your theoretical ODE baseline.
- A trace should be ACCEPTED (clean) if:
  a) Neither population ever drops below 0.0 (non-physical).
  b) The Mean Squared Error (MSE) between the observational data and the theoretical ODE baseline (interpolated to the same time points) is less than 5.0 for both prey and predator populations.
- A trace should be REJECTED (evil) if it violates any of the above conditions.
- Accepted CSV files must be copied to `<output_dir>/accepted/`.
- Rejected CSV files must be copied to `<output_dir>/rejected/`.

For your testing, you are provided with two directories of observational traces:
- `/app/corpora/clean/`: Contains 20 physically sound, low-noise traces.
- `/app/corpora/evil/`: Contains 20 corrupted, non-physical, or wildly unstable traces.

Your filter must successfully accept all files from the clean corpus and reject all files from the evil corpus. You can use these directories to perform regression testing on your `trace_filter.py` implementation.