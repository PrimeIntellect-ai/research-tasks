You are acting as an AI assistant for a machine learning engineer. I need you to write a C++ program to optimize a linear feature transformation matrix for our training data using Gradient Descent, and perform a regression test on it.

We have a dataset representing 3D features, and we need to align it with a target distribution by finding a 3x3 transformation matrix `W`.

Here are the requirements:
1. **Workspace**: All work should be done in `/home/user/ml_data`. I have already placed `train_X.txt`, `train_Y.txt`, `test_X.txt`, and `test_Y.txt` in this directory. Each file contains 100 rows and 3 columns of floating-point numbers (space-separated). 
2. **Algorithm**: You must write a C++ program `align.cpp` from scratch (without external libraries like Eigen; use standard multi-dimensional array manipulation using `std::vector` or raw arrays) that implements Gradient Descent to find `W`.
    * The Loss function is the Mean Squared Error: $L = \frac{1}{N} \sum_{i=1}^N \| X_i W - Y_i \|_2^2$
    * The gradient with respect to W is: $\frac{\partial L}{\partial W} = \frac{2}{N} X^T (X W - Y)$
    * Initialize `W` as a 3x3 matrix of zeros.
    * Learning rate ($\alpha$): 0.05
    * Iterations: 2000
3. **Program Interface**: Your compiled C++ program (`align`) should accept four command-line arguments: `<input_X_file> <input_Y_file> <output_W_file> <num_samples>`.
4. **Regression Testing**: To ensure your multi-dimensional array math and gradient steps are correct, first run your program on `test_X.txt` and `test_Y.txt` (which have 20 samples) and output to `test_W_out.txt`. The expected result for the test set is stored in `test_W_expected.txt`. Check that your output matches the expected matrix (within a small tolerance like 1e-4) before proceeding.
5. **Final Execution**: Once the regression test passes, run your program on `train_X.txt` and `train_Y.txt` (which have 100 samples) to produce `final_W.txt`.
6. **Output Format**: The output files (`test_W_out.txt` and `final_W.txt`) must contain exactly 3 rows of 3 space-separated floating-point numbers, formatted to exactly 6 decimal places.

Please write the C++ code, compile it, run the regression test, and finally generate `/home/user/ml_data/final_W.txt`.