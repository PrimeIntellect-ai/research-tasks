You are a Machine Learning Engineer preparing training data for a physics-informed neural network. The network learns the dynamics of a 3D harmonic oscillator system. However, the raw data we collected from a faulty sensor pipeline contains physical anomalies and corrupted trajectories. If we train on this "evil" data, our model will fail to conserve energy and produce divergent simulations.

Your task is to create a high-performance data filter in C that classifies trajectory files as either "clean" (physically valid) or "evil" (physically invalid).

**Task Details:**
1. **The Rule:** The physical rule and the maximum allowed energy threshold for a valid trajectory are written in an image artefact left by the lead physicist. You can find this image at `/app/system_rules.png`. You must extract the energy formula and the specific threshold from this image.
2. **The Source Code:** A partial C project is located at `/app/src/`. It contains `main.c`, `particle.h`, and a `Makefile`. You need to:
   - Implement the `int validate_particles(Particle* p, int count)` function inside `main.c` based on the rule extracted from the image.
   - The file contains thousands of particles per trajectory. You *must* accelerate the `validate_particles` loop using OpenMP.
   - Fix the `Makefile` to correctly link OpenMP and compile the scientific software from source.
3. **The Data:** 
   - A set of known good files is in `/app/corpus/clean/`.
   - A set of known anomalous files is in `/app/corpus/evil/`.
   - Each file contains a header with an integer `N` (number of particles), followed by `N` lines of `x y z vx vy vz` (all floating-point numbers).
4. **Integration:** 
   - Compile the program and place the final executable exactly at `/home/user/filter`.
   - The executable must take a single argument (the path to a data file).
   - `filter <file_path>` must exit with code `0` if the file is cleanly validated (all particles strictly obey the energy limit), and exit with code `1` if the file is evil (at least one particle exceeds the energy limit or violates the rules).

Build the filter, verify it against the corpora, and ensure the compiled binary is ready at `/home/user/filter`. Do not modify the data files themselves.