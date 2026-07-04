I need you to prepare a deterministic synthetic data generator for our physics-informed neural network training pipeline. 

We are simulating a 1D ring of coupled harmonic oscillators (a wave equation with damping). Our previous data generator used parallel iteration across the nodes, but because floating-point addition is non-associative, the parallel reduction order caused slight non-reproducibilities in our dataset. 

Here is your task:

1. **Audio Decoding**: I've left a voice memo at `/app/voicemail.wav` detailing the default parameters for the training set. Please transcribe this audio. Save the extracted parameters in `/home/user/default_params.txt` in the format `f0=<value>, damping=<value>`. (You can install dependencies like `ffmpeg` or Python audio transcription libraries to do this).

2. **Deterministic Generator**: Write a Rust program in `/home/user/data_gen` that compiles to a binary named `data_gen` (e.g., run `cargo build --release`). 
   - The binary must accept exactly four arguments in this order: `<N> <f0> <damping> <steps>`.
     - `N`: integer, number of nodes.
     - `f0`: float, base frequency.
     - `damping`: float, damping coefficient.
     - `steps`: integer, number of Euler integration steps.
   - Initial state for node `i` (from `0` to `N-1`):
     - Position `x[i] = sin(2.0 * PI * f0 * (i as f64) / (N as f64))`
     - Velocity `v[i] = 0.0`
   - **Integration Step** (Strictly sequential, single-threaded Euler method with `dt = 0.01`):
     - For each step from `0` to `steps - 1`:
       - First, calculate new velocities for all `i`. The force on node `i` is `(x[left] - 2.0 * x[i] + x[right]) - damping * v[i]`. (Use periodic boundary conditions: `left` is `i-1` wrapped around, `right` is `i+1` wrapped around). `v_new[i] = v[i] + force * 0.01`.
       - Second, update positions: `x[i] = x[i] + v_new[i] * 0.01`. Update the velocities to `v_new`.
   - **Output**: The program should print the *final* positions of all `N` nodes as a single comma-separated string on standard output, formatted to exactly 6 decimal places (e.g., `0.123456,-0.654321,0.000000`). No spaces, no brackets, just the numbers.

Please make sure your Rust code is robust, strictly sequential for determinism, and perfectly adheres to the math described above. I have an oracle binary that will test your executable with thousands of random inputs to ensure exact equivalence.