You are an AI assistant acting as a computational biologist and data scientist. Your task is to implement a kinetic model of primer-target DNA binding, incorporating sequence alignment to determine the reaction rate, and perform a numerical stability analysis of the integration.

You need to write a C program to do the following:

**1. Primer Sequence Alignment**
Given a target DNA sequence and a primer sequence, find the best local alignment score (without gaps) by sliding the primer across the target. 
- Target sequence: `ATGCGATCGATCGATCGATCGATCGATCGATC`
- Primer sequence: `GATCGATC`
- Scoring: +1 for a match, -1 for a mismatch.
- The alignment score $S$ is the maximum score found over all possible starting positions of the primer on the target.

**2. Kinetic Modeling (ODE Integration)**
Model the formation of the primer-target complex $C$ over time $t$ using the following ordinary differential equation:
$$\frac{dC}{dt} = k_{on} (P_0 - C)(T_0 - C) - k_{off} C$$
Where:
- Initial complex concentration $C(0) = 0.0$
- Initial primer $P_0 = 1.0$
- Initial target $T_0 = 1.0$
- Forward rate $k_{on} = S \times 1000$ (where $S$ is the best alignment score)
- Reverse rate $k_{off} = 0.1$

Integrate this ODE from $t = 0$ to $t = 0.01$ seconds using the **standard 4th-order Runge-Kutta (RK4)** method.

**3. Numerical Stability Testing**
Because the rate constant $k_{on}$ can be large, the ODE might be stiff. You must test the following integration time steps ($dt$): `0.1`, `0.01`, `0.001`, `0.0001`, and `0.00001`.
For each $dt$, run the RK4 integration from $t=0$ to $t=0.01$. 
An integration is considered **stable** if and only if the complex concentration $C$ remains strictly within the physically meaningful bounds $0.0 \le C \le 1.0$ at *every* step of the integration, and does not yield NaN. 
Identify the *largest* $dt$ from the list above that results in a stable integration.

**4. Orchestration and Output**
Write, compile, and execute your C program (e.g., `model.c`) in `/home/user`. 
Your program or an accompanying shell script must generate a final JSON report at `/home/user/results.json` with exactly this structure:

```json
{
  "best_score": <integer>,
  "largest_stable_dt": <float>,
  "final_C_at_stable_dt": <float rounded to 4 decimal places>
}
```

Ensure all files are created in `/home/user`. Do not use external libraries other than the standard C math and standard I/O libraries.