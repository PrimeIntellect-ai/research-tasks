You are helping a data science researcher who is organizing a large tabular dataset of experimental results. They have an old legacy binary `/app/oracle_scorer` that processes data points and assigns a "Data Quality Score" (an integer) and a "Category" (an integer class) based on 4 experimental parameters. 

Unfortunately, the source code for this binary was lost. The researcher needs to integrate this scoring logic into a modern Go-based data pipeline. 

Your task is to reverse-engineer the mathematical model inside the legacy binary and write a bit-exact equivalent implementation in Go.

The legacy binary is a stripped executable. It takes exactly 4 integers as command-line arguments (let's call them A, B, C, D, all generally between -100 and 100) and prints two integers separated by a space: the `Score` and the `Category`.
Example: `/app/oracle_scorer 10 20 30 40`

To accomplish this, you should:
1. Write a script to probe `/app/oracle_scorer` with a structured set of random inputs to generate a tabular dataset.
2. Use statistical modeling and regression techniques (you may install Python and `scikit-learn`/`statsmodels`, or use Go's `gonum` numerical library) to perform an exploratory analysis and deduce the exact mathematical relationships. Hint: The score is based on a clean mathematical formula (regression), and the category is a mathematical classification based on the score or inputs. Use hypothesis testing on your model's residuals to confirm you have the exact formula.
3. Write a Go program at `/home/user/solution.go` that takes 4 integer command-line arguments and prints the exact same `<Score> <Category>` string as the oracle.
4. Compile your Go program to `/home/user/solution`.

The automated verifier will randomly fuzz your `/home/user/solution` against the `/app/oracle_scorer` with thousands of inputs to ensure absolute bit-exact equivalence. Do not approximate; find the exact integer coefficients and logic.