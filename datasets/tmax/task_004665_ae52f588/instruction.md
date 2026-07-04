Hi there, I'm a researcher running some biochemical simulations and I'm running into numerical stability issues. My forward Euler integrator keeps diverging because the step-size adaptation is wrong, and I just want to find the maximum fixed step size I can use before the simulation blows up.

I have a PDB file at `/home/user/enzyme.pdb`. I need you to do the following:

1. Parse the `/home/user/enzyme.pdb` file. Extract the Z-coordinates of all `ATOM` records and calculate their mean. This value will be the initial condition, $y_0$.
2. We are simulating the decay of a compound using the ordinary differential equation:
   $$ \frac{dy}{dt} = -0.1 y^3 $$
3. Implement a Forward Euler numerical integrator for this ODE from $t = 0$ to $t = 10$. 
   (Your integration loop should run as long as the current time $t < 10$. Update time by $t_{new} = t + h$).
4. The simulation is considered "stable" if the absolute value of $y$ never exceeds $1000$ during the integration.
5. Write a Python script to systematically test and find the **maximum stable step size** $h$ for this integration. Test step sizes in increments of exactly $0.001$, starting from $0.001$ upwards.
6. Once you find the maximum stable step size $h$ (a float with 3 decimal places, e.g., 0.123), write this exact value to a file at `/home/user/max_step.txt`.

Please perform this task. You can write and execute any scripts you need in `/home/user`.