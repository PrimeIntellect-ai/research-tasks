You are tasked with fixing a broken build pipeline for a physical simulation engine written in Rust. The project is located at `/home/user/sim_engine/`. Currently, the project fails to compile because it is missing a generated file: `src/trajectory_constants.rs`. 

The pipeline is supposed to analyze a video of a physical experiment, extract the movement parameters, and bake them into the compiled Rust binary.

Here are your instructions:
1. You have a video fixture located at `/app/experiment.mp4`. The video contains a black dot moving in a parabolic trajectory on a white background (resolution: 640x480). 
2. Write a Python script at `/home/user/extract_math.py` that implements a numerical algorithm to read the video frames, detect the centroid of the black dot (using libraries like `opencv-python` and `numpy`), and fit a polynomial $y = Ax^2 + Bx + C$ to the path. Note: Assume pixel coordinates where $x$ is the horizontal axis (0 to 640) and $y$ is the vertical axis (0 to 480, top-left origin).
3. The Python script must generate the missing Rust file at `/home/user/sim_engine/src/trajectory_constants.rs` with the following exact structure:
```rust
pub const COEFF_A: f64 = <your_A_value>;
pub const COEFF_B: f64 = <your_B_value>;
pub const COEFF_C: f64 = <your_C_value>;
```
4. Orchestrate an end-to-end pipeline: write a bash script at `/home/user/ci_pipeline.sh` that installs any necessary Python dependencies, runs `/home/user/extract_math.py`, and then executes `cargo build` and `cargo test` in the `/home/user/sim_engine/` directory.

Ensure your mathematical fitting is accurate, as the Rust tests (and our automated grading) have strict numerical thresholds on the coefficients.