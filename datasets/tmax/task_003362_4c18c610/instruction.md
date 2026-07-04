I am trying to fit a basic harmonic oscillator model to some experimental video data, but my numerical integrator keeps diverging. 

I have a video of a flashing signal at `/app/signal.mp4`. I also have a pipeline script at `/home/user/run_model.sh` that is supposed to:
1. Extract the average frame intensity from the video over time.
2. Find the dominant frequency $f$ of the flashing signal using an FFT script (`/home/user/fft.py`).
3. Solve the harmonic oscillator ODE $y'' = - \omega^2 y$ (where $\omega = 2\pi f$) using a Bash-based numerical integrator, starting at $y(0)=1, y'(0)=0$.
4. Save the output to `/home/user/trajectory.tsv` (tab-separated, columns: `Time`, `Position`) from $t=0$ to $t=2.0$ seconds.

Unfortunately, the Bash-based Euler integrator in `run_model.sh` diverges wildly because it uses standard explicit Euler with a time step (`dt=0.1`) that is too large for the frequency of the signal. 

Please fix `/home/user/run_model.sh` so that it:
1. Correctly calculates the frequency from the video.
2. Modifies the ODE integration loop to use the **Semi-Implicit Euler** method (which is stable for oscillating systems) and an appropriately small time step (e.g., `dt=0.01`).
3. Outputs the correctly simulated trajectory to `/home/user/trajectory.tsv`.

Run the fixed script to generate the final `trajectory.tsv`.