You are acting as a machine learning engineer preparing training data. We need to generate a synthetic dataset, compute its linear regression, and visualize it. 

I have placed a C source file at `/home/user/data_gen.c`. This program simulates an experimental data generator by solving a nonlinear equation ($y^3 + y - x = 0$) for various $x$ values using Newton's method.

Your task is to:
1. Compile `/home/user/data_gen.c` into an executable named `/home/user/data_gen` using `gcc`.
2. Run `/home/user/data_gen` and save its output to `/home/user/dataset.csv`. The output will contain `x,y` pairs.
3. Write a Go program at `/home/user/process.go` that:
   - Reads `/home/user/dataset.csv`.
   - Computes the linear regression coefficients ($m$ and $c$ for the line $y = mx + c$) using least squares.
   - Generates an SVG visualization of the experimental data points (as small circles) and the fitted linear regression line. Save this plot to `/home/user/plot.svg`.
   - Writes the calculated $m$ and $c$ to `/home/user/regression.txt` in the exact format:
     ```
     m=<value>
     c=<value>
     ```
     (Round the values to 4 decimal places).

Ensure your Go code is self-contained and uses standard libraries where possible. You can run your Go code to produce the required output files.