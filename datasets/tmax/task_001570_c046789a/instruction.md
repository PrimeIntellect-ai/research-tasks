You are a data scientist tasked with implementing a fast numerical solver for a pharmacokinetic compartment model. 

A colleague has left the specification of the model in an image file located at `/app/model_spec.png`. The image contains text detailing a system of Ordinary Differential Equations (ODEs), the specific rate constants (`k1`, `k2`), initial conditions, the numerical integration method to use, and the step size (`dt`).

Your task is to:
1. Extract the model specifications from `/app/model_spec.png` (Tesseract OCR is installed on the system).
2. Initialize a new Rust project at `/home/user/pk_solver`.
3. Implement the numerical integration method specified in the image to solve the ODE system. 
4. Your Rust program must be compiled in release mode. The final executable should be located at `/home/user/pk_solver/target/release/pk_solver`.

**Executable Interface Specification:**
- The executable must read from standard input (`stdin`).
- It will receive a sequence of integers, one per line. Each integer `N` represents the number of integration steps (of size `dt`) to simulate starting from `t = 0` and the initial conditions.
- For each integer `N`, your program must compute the state of the system after `N` steps.
- The output must be written to standard output (`stdout`), one line per input `N`, containing the values of the variables `y` and `z` separated by a comma.
- Both `y` and `z` must be formatted to exactly 6 decimal places.
- The simulation for each `N` should be independent (always starting from the initial conditions at `t=0`). 

**Constraints:**
- You must write the implementation in Rust.
- Do not use pre-built numerical integration crates (like `ode_solvers`). Implement the specified algorithm from scratch.
- Ensure your output matches standard rounding rules for 6 decimal places.

Begin your work by analyzing the image and writing the solver!