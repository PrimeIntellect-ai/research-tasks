You are an AI assistant helping a computational physics researcher. The researcher is studying a damped nonlinear pendulum system and has a directory of simulation parameter files, but many of the configurations are physically incorrect or numerically unstable. 

Your task has three parts:

**1. Video Analysis**
The researcher recorded the real-world pendulum experiment. The video is located at `/app/experiment_video.mp4`. 
Extract the frames (you may use `ffmpeg`, which is available) and write a short script (Python or C++) to analyze the motion and determine the dominant oscillation frequency (in Hz) of the system. The video shows a bright white blob (the pendulum bob) swinging on a dark background.

**2. C++ ODE Simulator & Classifier**
Write a C++ program named `/home/user/verifier.cpp` (and compile it to `/home/user/verifier`) that takes a single command-line argument: the path to an HDF5 configuration file. 

Each HDF5 file contains the following double-precision floating-point datasets at the root group:
- `gamma`: The damping coefficient.
- `omega_sq`: The squared natural frequency ($\omega_0^2$).
- `dt`: The time step size for the simulation.
- `t_max`: The total simulation time.

Your C++ program must:
a. Read these datasets using the HDF5 C++ API.
b. Simulate the damped nonlinear pendulum ODE: $\frac{d^2\theta}{dt^2} = -\gamma \frac{d\theta}{dt} - \omega_{sq} \sin(\theta)$
c. Use the 4th-order Runge-Kutta (RK4) method. The initial conditions are $\theta(0) = 1.0$ and $\frac{d\theta}{dt}(0) = 0.0$. 
d. **Numerical Stability Test:** Track the state variables. If at any point during the simulation $|\theta| > 100.0$ or the values become NaN/Inf (which happens if `dt` is too large for the stiffness of the system), the simulation is numerically unstable.
e. **Validation:** If the simulation completes stably, estimate the oscillation frequency from the simulated time series (e.g., by counting zero-crossings or peak-to-peak times). 

**Decision Logic:**
- If the simulation is numerically unstable: REJECT (exit with code `1`).
- If the simulation is stable, but the simulated frequency differs from the video's actual frequency by more than $\pm 10\%$: REJECT (exit with code `1`).
- If the simulation is stable AND the simulated frequency matches the video frequency within $\pm 10\%$: ACCEPT (exit with code `0`).

**3. Integration & Testing**
You have two datasets of HDF5 files provided by the researcher:
- `/app/corpus/clean/`: These files should all be ACCEPTED.
- `/app/corpus/evil/`: These files should all be REJECTED (either unstable or wrong frequency).

Install any necessary development packages (like `libhdf5-dev`), compile your C++ program, and test it against the corpora. Ensure your program strictly follows the exit code contract so it can be used as an automated filter.