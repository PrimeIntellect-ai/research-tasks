You are tasked with fixing a bioinformatics simulation tool written in Rust.

The project is located at `/home/user/seq_model`. It models the competitive dynamics of three microbial sequences using a system of Ordinary Differential Equations (ODEs). The tool performs numerical integration to project the sequence concentrations from $t=0$ to $t=5.0$.

Currently, if you run the simulation (`cargo run`), the output diverges to `NaN` because the step-size adaptation logic in the numerical integrator is flawed. The developer accidentally inverted the adjustment multipliers: it increases the step size when the error is too high, and decreases it when the error is acceptable!

Your task is to:
1. Identify the adaptive ODE solver in `/home/user/seq_model/src/main.rs`.
2. Fix the step-size adaptation logic. Specifically:
   - When the error exceeds the tolerance, the step size `dt` should be **halved** (`dt *= 0.5`).
   - When the error is within the tolerance, the state should advance, and the step size `dt` should be **increased by 20%** for the next step (`dt *= 1.2`).
3. Compile and run the fixed Rust project.
4. The program will print out the final concentration vector at $t=5.0$. Save this final 3-element vector as a comma-separated list of numbers (e.g., `10.123,5.456,2.789`) into a file named `/home/user/final_population.txt`. 

Make sure the program completes successfully without `NaN` or `inf` values.