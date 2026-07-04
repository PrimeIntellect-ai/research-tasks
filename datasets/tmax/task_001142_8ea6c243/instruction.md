You are a research assistant tasked with restoring a legacy simulation pipeline that must run on a highly restricted compute node containing only standard POSIX tools, bash, coreutils, tesseract, and netcat (no Python, R, or C++ compilers).

We have an image of the physical coefficients for our model saved at `/app/system_params.png`.

Your objectives are:
1. **Parameter Extraction**: Use `tesseract` to read the image at `/app/system_params.png`. It contains a line with the format `COEFFICIENTS: ALPHA=<val> BETA=<val>`. 
2. **Environment & Tooling**: Create a directory `/home/user/sim_env`. Write all your scripts here. 
3. **Numerical Integration (`integrate.sh`)**: Write a bash script that uses `awk` or `bc` to compute the definite integral of the function `f(x) = ALPHA * x^2 + BETA * x` from `x=0` to a given upper limit `X`. Use the trapezoidal rule with `N=1000` steps. The script should take `X` as its only command-line argument and print only the final computed float value.
4. **Density Estimation & Visualization (`density.sh`)**: Write a bash script that generates 5000 uniform random numbers between 0 and 100. Bin these numbers into 10 equal-width intervals (0-10, 10-20, ..., 90-100). The script must output an ASCII histogram where each line is formatted as `[bin_start]-[bin_end]: <count>`.
5. **Network Service (`server.sh`)**: We need a way to query these models remotely. Implement a basic TCP server listening on `127.0.0.1:8080` using `nc` (netcat) or `socat` in a loop. It must handle two types of raw text requests:
   - Request exact text: `INTEGRATE <X>` (e.g., `INTEGRATE 5.5`) -> The server must respond with the result of `integrate.sh 5.5` followed by a newline.
   - Request exact text: `DENSITY` -> The server must respond with the output of `density.sh`.

You must start the server in the background so it is running and listening on `127.0.0.1:8080` when you consider the task complete. The server must accept multiple sequential connections. Leave the background process running.