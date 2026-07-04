You are helping our data science team fix a legacy model-fitting pipeline. The core of this pipeline is a numerical integrator written entirely in Bash and Awk, located at `/home/user/adaptive_integrator.sh`. 

This script solves the non-linear ordinary differential equation:
dy/dt = -y^2 + t

It uses an adaptive Euler method, but the current step-size adaptation logic is broken, causing the integration to diverge or take too many steps. 

We found a scanned note from the original author in `/app/params.png`. You need to:
1. Extract the required error tolerance (`TOL`) parameter from `/app/params.png`.
2. Fix the step-size adaptation logic in `/home/user/adaptive_integrator.sh`. The correct adaptation formula for Euler is: `h_new = h_old * 0.9 * sqrt(TOL / err)`. (Assume `err` is the absolute difference between a full-step Euler and two half-step Eulers, which is already calculated in the script as `err`).
3. Ensure the step size `h` never exceeds 0.5 and never falls below 1e-5.
4. The script takes three arguments: initial value `y0`, end time `t_end`, and initial step size `h0`. The initial time is always `t=0`.
5. The script must output a single line with two space-separated values: the final computed `y(t_end)` (rounded to 5 decimal places) and the total number of accepted steps.

Please fix `/home/user/adaptive_integrator.sh` so it correctly implements this logic. An automated system will fuzz your script with hundreds of random `y0`, `t_end`, and `h0` values to ensure it is bit-exact equivalent to our reference implementation.

Note: You may need to install `tesseract-ocr` or similar tools to read the image. Ensure your Bash script is executable and robust.