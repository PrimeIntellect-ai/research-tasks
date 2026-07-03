You are assisting a researcher who is running numerical simulations of a damped mechanical system. The principal investigator left the critical damping parameter encoded as a sequence of DTMF (Dual-Tone Multi-Frequency) tones in an audio file before leaving for an expedition. 

Your task consists of two parts:

Part 1: Signal Processing (Parameter Extraction)
Analyze the audio file located at `/app/parameter.wav`. It contains a sequence of DTMF tones representing a floating-point number. In this sequence, the asterisk tone (`*`) was used to represent the decimal point. Extract this numerical value (let's call it $D$).

Part 2: Nonlinear Solver Implementation
Write a Python script at `/home/user/solver.py` that uses the extracted parameter $D$ to process scientific simulation data. 
Your script must meet the following specifications:
- It will be executed via the command line and take exactly one argument: the path to an HDF5 file. (e.g., `python3 /home/user/solver.py /tmp/sim_data.h5`)
- It must open the HDF5 file and read the dataset located at the internal path `/data/signal`. This dataset contains a 1D array of floating-point numbers.
- Calculate the arithmetic mean of this array, let's call it $M$.
- Solve the following non-linear equation for the real root $x$:  
  $x^3 + D \cdot x - M = 0$
- Output *only* the real root $x$, rounded to exactly 5 decimal places (e.g., `1.23456`), to standard output. Do not print any other text, warnings, or debug information.

Ensure your root-finding method is numerically stable, as $M$ can range anywhere from -1000.0 to 1000.0.