You are assisting a marine acoustics researcher who is filtering out anomalous outputs from a massive Monte Carlo simulation of underwater sound propagation.

The simulation outputs observational data and Monte Carlo energy samples into HDF5 files. Unfortunately, due to sensor glitches and numerical instability, some of the generated files are corrupted or represent non-physical states. 

You need to create a Rust-based command-line tool that acts as a strict validator (filter) for these HDF5 files.

Here is the specification for the validation:
1. The tool must be written in Rust, located at `/home/user/sim_filter`, and compiled in release mode (so the binary is at `/home/user/sim_filter/target/release/sim_filter`).
2. The executable must take a single argument: the path to an HDF5 file.
3. It must exit with status code `0` if the file is completely valid, and a non-zero status code (e.g., `1`) if the file violates ANY of the constraints.
4. **Constraints for a valid file:**
   - The HDF5 file must contain the dataset `/observational/metadata`. If this dataset is missing, the file is invalid.
   - The dataset `/mc_results/energy` (a 1D array of floats) must NOT contain any negative values. (Energy cannot be negative).
   - The dataset `/mc_results/amplitude` (a 1D array of floats) must have a peak (maximum) value strictly less than a specific threshold.
5. **Finding the Threshold:** The researcher left an audio note detailing the exact amplitude threshold for this batch of simulations. The audio file is located at `/app/hydrophone_metadata.wav`. You must transcribe or listen to this file to obtain the numerical threshold.

The researcher has provided a test corpus of simulation outputs:
- `/app/sim_corpus/clean/` contains valid HDF5 files.
- `/app/sim_corpus/evil/` contains anomalous/corrupted HDF5 files.

Your Rust program will be evaluated against these two directories. It must accept (exit 0) all files in the `clean` directory and reject (exit non-zero) all files in the `evil` directory. 

Write the Rust tool, build it, and test it against the provided corpus. Ensure your final binary is at `/home/user/sim_filter/target/release/sim_filter`.