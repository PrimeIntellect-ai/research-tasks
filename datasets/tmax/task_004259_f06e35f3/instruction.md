You are a machine learning engineer preparing training data for a biophysics model. A colleague was working on a pipeline to simulate protein folding kinetics, but their numerical integrator keeps diverging, ruining the training dataset.

Your colleague left the following files:
1. `/app/lab_notes.wav`: An audio voice memo containing the correct numerical parameters they discovered before they left.
2. `/home/user/protein.pdb`: A PDB file of the target protein.
3. `/home/user/sim_kinetics.py`: A script that reads the initial condition, runs an ODE simulation, and outputs `trajectory.csv`.

Your tasks are:
1. **Audio Transcription:** Listen to or transcribe `/app/lab_notes.wav` to find the correct integration tolerance required to prevent divergence.
2. **Bioinformatics Parsing:** The initial condition for the simulation (variable `Y0`) must be dynamically set to the exact number of amino acid residues in `/home/user/protein.pdb`. 
3. **Simulation Refinement:** Edit `/home/user/sim_kinetics.py` to replace the diverging fixed-step Euler method with an adaptive step-size integrator (e.g., `scipy.integrate.solve_ivp`). Apply the tolerance you extracted from the audio memo.
4. **Data Generation:** Run the fixed script to generate `/home/user/trajectory.csv`. It must contain two comma-separated columns: `t` and `y`, evaluated from `t=0` to `t=10` at exactly 100 evenly spaced points (including endpoints).

The underlying analytical equation the script is trying to simulate is $dy/dt = -0.5 \cdot y$. 
Your final generated `trajectory.csv` will be evaluated programmatically against the exact analytical solution. The Mean Squared Error (MSE) must be extremely low.