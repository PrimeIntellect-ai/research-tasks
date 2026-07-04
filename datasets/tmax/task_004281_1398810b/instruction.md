You have just inherited an unfamiliar codebase located in `/home/user/project`. The previous developer left behind a Python script `solver.py` and a data file `data.bin`, but no documentation.

The script is supposed to read an array of floats from the binary file, compute their mean, and then use gradient descent to find the optimal parameter `x` that minimizes the quadratic function `f(x) = x^2 - mean * x`. 

However, there are several issues:
1. **Statistical Anomaly**: The mean being calculated is wildly incorrect (producing massive, seemingly random values). We suspect the binary data reader is completely broken and reading the wrong types or offsets. You will need to reverse-engineer the binary format of `data.bin` (hint: look for a file magic header, an element count, and figure out the correct floating-point precision).
2. **Convergence Failure**: The optimization loop diverges. Instead of settling on a minimum, the value of `x` explodes to infinity (or `NaN`). 

Your task is to debug and fix `solver.py` so that it correctly parses `data.bin`, computes the true statistical mean, and successfully converges on the optimal parameter.

Once fixed, run the script so it generates `/home/user/project/output.txt`.

The format of `/home/user/project/output.txt` should be:
```
Mean: <calculated_mean_to_4_decimal_places>
Opt: <optimized_x_to_4_decimal_places>
```

Do not change the output file location or formatting.