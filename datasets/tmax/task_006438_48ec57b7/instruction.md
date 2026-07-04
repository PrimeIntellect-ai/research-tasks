You are an AI assistant helping a data scientist debug a model fitting pipeline.

We are trying to fit a linear model to some spectroscopy signal data mapped to protein sequences. The C++ program `/home/user/model/fit_model.cpp` reads signal features from `/home/user/model/signals.csv` and target sequence lengths from `/home/user/model/proteins.fasta`.

The model is trained using Ordinary Least Squares (OLS) via the normal equation: 
$w = (X^T X)^{-1} X^T y$

However, the program is currently failing. The signal data has highly correlated baseline artifacts, making the matrix $X^T X$ near-singular. The matrix inversion function fails and terminates the program.

Your task:
1. Modify `/home/user/model/fit_model.cpp` to implement Ridge Regression. You must add a regularization parameter $\lambda = 0.1$ to the main diagonal of the $X^T X$ matrix *before* it is inverted.
2. The code already contains a function to parse the sequence lengths from `proteins.fasta` and read the `signals.csv`. You only need to add the ridge penalty logic and ensure the code compiles successfully.
3. Compile the program using `g++ -std=c++11 /home/user/model/fit_model.cpp -o /home/user/model/fit_model`.
4. Run the program. It should output the computed 4-dimensional weight vector.
5. Save the output weights to `/home/user/weights_output.txt`. The file should contain exactly 4 floating point numbers, separated by spaces, formatted to 4 decimal places.

Ensure you do not alter the sequence parsing or file reading logic, only the mathematical formulation for $X^T X$.