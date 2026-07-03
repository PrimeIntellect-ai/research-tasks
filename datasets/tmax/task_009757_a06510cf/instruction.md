You are helping a computational chemistry researcher fix a data processing pipeline for their spectroscopy simulations. 

The researcher has a Rust project at `/home/user/spectro_solve` that orchestrates a workflow comparing simulated mixture spectra against reference datasets to determine component concentrations. It relies on solving a linear system derived from the Beer-Lambert law at two specific wavelengths. 

Currently, the workflow is failing its test suite because the 2x2 linear equation solver has a mathematical bug.

Your task:
1. Navigate to `/home/user/spectro_solve`.
2. Inspect `src/lib.rs` and identify the logical bug in the `solve_concentrations` function (it uses Cramer's rule to solve a 2x2 system but contains a typo).
3. Fix the bug so that `cargo test` passes. The test compares the solver output against a known reference dataset.
4. Once the tests pass, run the binary to process the main dataset: `cargo run --release > /home/user/concentrations.txt`.

The final file `/home/user/concentrations.txt` must contain the output of the fixed program. Do not modify the tests or the `main.rs` file, only fix the solver logic in `lib.rs`.