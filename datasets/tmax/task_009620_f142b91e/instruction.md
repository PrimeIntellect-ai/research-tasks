You are an AI assistant helping a data scientist fix and automate a model-fitting pipeline. 

We are trying to fit a simple linear model that requires solving a 2x2 system of equations $Ax = b$. However, the input matrices we receive are often near-singular, causing our standard exact solver to fail or produce wildly unstable results.

Your task is to build a reproducible pipeline to solve this issue:

1. **Write a C program (`/home/user/workspace/solver.c`)**:
   Create a C program that takes 7 command-line arguments (as floating-point numbers) in this exact order: 
   `A00 A01 A10 A11 b0 b1 lambda`
   The program must add the regularization parameter `lambda` to the main diagonal of the 2x2 matrix $A$ (i.e., $A_{00} \rightarrow A_{00} + \lambda$ and $A_{11} \rightarrow A_{11} + \lambda$). Then, solve the linear system $(A + \lambda I)x = b$ using Cramer's rule. 
   The program should print the solution as two space-separated floats with 6 decimal places (e.g., `0.598802 1.197605`) to standard output.

2. **Write a Jupyter Notebook (`/home/user/workspace/pipeline.ipynb`)**:
   Create a Python Jupyter notebook that orchestrates the regression testing. The notebook must:
   - Use the `subprocess` module to call the compiled C executable (`/home/user/workspace/solver`).
   - Pass the singular matrix elements `1.0 2.0 2.0 4.0`, the right-hand side `3.0 6.0`, and a lambda of `0.01`.
   - Capture the output string.
   - Parse the output into a Python dictionary with keys `"x0"` and `"x1"`.
   - Write this dictionary to a JSON file at `/home/user/workspace/results.json`.

3. **Create a pipeline script (`/home/user/workspace/run_pipeline.sh`)**:
   Write a bash script that:
   - Compiles `solver.c` into an executable named `solver` in the same directory using `gcc`.
   - Executes the Jupyter notebook from the command line without opening a GUI (use `jupyter nbconvert --execute --to notebook --inplace /home/user/workspace/pipeline.ipynb`).
   
Make sure the bash script is executable. You may need to install Jupyter in the system/environment if it's not present (use `pip install jupyter`). Ensure all files are placed in `/home/user/workspace`. Do not create any other extraneous files.