You are a machine learning engineer preparing feature data for a predictive model. You need to extract features from raw signal data and determine their linear relationship with the target variable using standard Linux tools and a custom C program. 

Your tasks are to:
1. Compile a C program located at `/home/user/src/calc_energy.c`. This program reads whitespace-separated floating-point numbers from standard input and prints the sum of their squares (the "energy" of the signal) formatted to 4 decimal places. Compile it to `/home/user/bin/calc_energy`. Make sure to create the `bin` directory if it doesn't exist.
2. Verify the compilation by running the regression test script `/home/user/src/test_energy.sh`. The script will output "PASS" if the program works correctly.
3. Process the raw signal dataset `/home/user/data/signals.txt`. Each line represents one signal. Use your compiled `calc_energy` program to compute the energy for each line.
4. The file `/home/user/data/targets.txt` contains the target variable for each signal (one float per line, matching the lines in `signals.txt`). 
5. Calculate the linear regression line $y = mx + b$ between the signal energy ($x$) and the target variable ($y$). You must do this using a bash script or `awk`. Do not use Python or R.
6. Save the final slope ($m$) and intercept ($b$) to `/home/user/regression_results.txt` in exactly this format:
`Slope: <m>, Intercept: <b>`
Format both numbers to 4 decimal places.

Linear regression formulas for reference:
$m = \frac{N \sum(xy) - \sum(x)\sum(y)}{N \sum(x^2) - (\sum x)^2}$
$b = \frac{\sum(y) - m \sum(x)}{N}$
where $N$ is the number of samples.