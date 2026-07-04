I am working on a machine learning pipeline where I need to prepare a mathematical dataset and evaluate a simple baseline polynomial model in C++. 

I have written a C++ program at `/home/user/prepare_data.cpp` that reads raw training data from `/home/user/raw_data.csv`. The script is supposed to normalize the input feature `x` (using `max_x = 5`), compute polynomial features (`f1 = x_norm`, `f2 = x_norm^2`), and generate predictions using the formula `y_pred = 5.0 * f1 + 2.0 * f2`. Finally, it calculates the Mean Squared Error (MSE) between `y_pred` and the true `y` labels.

However, there is a misconfiguration in my code. When I look at the output, the generated features and predictions are essentially "blanked out" (evaluating to 0 for most rows), which makes the validation MSE completely incorrect. I suspect there is an issue with how the math is being computed.

Your task:
1. Identify and fix the numerical type/math bug in `/home/user/prepare_data.cpp` so the features and predictions compute accurately.
2. Compile the fixed script using `g++` into an executable named `/home/user/prepare_data`.
3. Run the executable to process the data.

When successfully run, the script should correctly populate `/home/user/features_output.csv` with the columns `x,f1,f2,y_pred` and output the correct error to `/home/user/mse.txt` formatted exactly as `MSE: <value>`.

Please make sure you only modify the bug itself, preserving the overall logic, file paths, and output formats.