You are a data scientist working on a reproducible computational pipeline to fit a biological model of a genetic oscillator. 

We have a C program located at `/home/user/biomodel.c`. This program simulates the concentration of a protein over time based on the binding efficiency of a specific primer. The binding efficiency is calculated by counting the number of times the primer sequence occurs in the target DNA sequence, which sets the stiffness parameter $k$ of the oscillator. 

Currently, the numerical integrator in `biomodel.c` is using the Forward Euler method with a hardcoded step size of `dt = 0.5`. Because of this large step size, the ODE integration diverges rapidly, yielding `NaN` or `Infinity` values due to poor step-size adaptation for stiff parameters.

Your tasks are:
1. Fix the C code in `/home/user/biomodel.c` by changing the integration time step `dt` to exactly `0.001` to ensure numerical stability.
2. The simulation simulates the system from $t = 0$ to $t = 10.0$. Do not change the total simulation time, just the `dt` and the number of steps required to reach $t = 10.0$.
3. Create a bash script at `/home/user/pipeline.sh` that takes exactly two arguments: the target DNA sequence and the primer sequence.
4. The bash script must:
    - Compile `/home/user/biomodel.c` into an executable named `/home/user/biomodel`.
    - Execute `/home/user/biomodel` with the provided target and primer sequences.
    - Capture the final simulated concentration of the protein `x` at $t = 10.0$ (which is printed to standard output by the C program as its final line).
    - Save ONLY this final numeric value (formatted to 4 decimal places, e.g., `-0.1234`) into a file called `/home/user/result.txt`.

Test your pipeline by running:
`bash /home/user/pipeline.sh ACGTACGTACGT ACGT`

Ensure that the final output in `/home/user/result.txt` contains only the numeric value.