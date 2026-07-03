As a performance engineer, we are analyzing a mechanical system whose failure is triggered by resonant frequencies when subjected to near-singular stress matrices. 

We have recorded a vibration signature of the system just before a previous failure, located at `/app/system_vibration.wav`. 

Your task is to write a highly optimized Python script located at `/home/user/fast_solver.py` that computes the system's stress response. The script must exactly replicate the behavior of our reference implementation (which is too slow).

The script must take exactly two command-line arguments:
1. The path to the audio file (`/app/system_vibration.wav`).
2. A comma-separated string of 4 floating-point numbers representing a 2x2 near-singular stress matrix (e.g., `1.0,2.0,2.0,4.01`).

The script must perform the following steps:
1. **Spectral Analysis**: Read the provided WAV file, compute its Fast Fourier Transform (FFT), and identify the single dominant frequency (in Hz, rounded to the nearest integer) where the magnitude is highest. Let this frequency be $f_d$.
2. **ODE Simulation**: Simulate the system's response using the differential equation:
   $dx/dt = v$
   $dv/dt = -k \cdot x - c \cdot v + A \cdot \sin(2 \pi f_d t)$
   Where $k = M_{00} \cdot M_{11}$, $c = M_{01} + M_{10}$ (from the input matrix $M$), and $A = 10.0$.
   Initial conditions: $x(0) = 0$, $v(0) = 0$.
   Integrate this from $t=0$ to $t=2.0$ seconds using Euler's method with a step size of $\Delta t = 0.001$.
3. **Output**: Print a single floating-point number representing the maximum absolute displacement `max(|x|)` observed during the simulation, rounded to exactly 4 decimal places.

Your script will be tested against our automated fuzzing infrastructure, which will feed it random near-singular matrices and expect identical output to our golden oracle. Make sure your script runs efficiently and handles standard input parsing without errors.