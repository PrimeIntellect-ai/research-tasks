You are a machine learning engineer preparing training data for a surrogate model. You have access to a high-fidelity physics simulator, but it is computationally expensive. Your goal is to intelligently sample the simulator to build a high-accuracy interpolant for the domain \( x \in [0, 1] \).

You have been provided with:
1. `/app/noisy_observations.dat`: A raw dataset of legacy observations in the format `id,x_val,y_val,timestamp`. The points are randomly scattered and contain significant observational noise.
2. `/app/simulator`: A stripped, black-box compiled binary of the high-fidelity simulator. It takes a single file argument containing a list of `x` values (one per line) and outputs the exact `y` values to standard output (one per line).

Your objectives are:
1. **Observational Data Reshaping**: Parse and reshape the raw `/app/noisy_observations.dat` to extract the `x` and `y` coordinates.
2. **Mesh Refinement**: Using the reshaped noisy data, estimate regions of high variability or sharp gradients. Based on this, generate an optimized non-uniform mesh of **exactly 150 points** in the domain `[0, 1]`. 
3. **Simulator Query**: Pass your optimized 150-point mesh to `/app/simulator` to obtain the true, noiseless values.
4. **Curve Fitting and Regression**: Write a C++ program (e.g., `/home/user/surrogate.cpp`) that takes these 150 exact points and performs linear interpolation to generate predictions for a dense uniform mesh of exactly 10,000 points in `[0, 1]` (where \( x_i = i / 9999.0 \) for \( i = 0, \dots, 9999 \)). Save these 10,000 predicted `y` values to `/home/user/predictions.txt` (one value per line).
5. **Bootstrap Confidence Intervals**: Calculate the mean of your 10,000 predicted values. Compute the 95% bootstrap confidence interval for this mean using 1,000 bootstrap resampling iterations. Save the lower and upper bounds to `/home/user/bootstrap_ci.txt` in the format `lower,upper`.

Criteria for success:
- Your final interpolant evaluated on the 10,000 uniform points (`/home/user/predictions.txt`) will be graded against the exact high-fidelity function values using Mean Squared Error (MSE). 
- To pass, your predictions must achieve an **MSE < 0.001**. A naive uniform mesh of 150 points will typically fail to capture the sharp peaks and result in an MSE higher than the threshold.
- The entire process should be scriptable and well-organized. You are free to use Python/bash for data reshaping and querying, but the main interpolation and prediction logic must be implemented in **C++**.