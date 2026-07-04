As a data scientist, you are analyzing a 2D response surface. You have been given a dataset in `/home/user/data.txt` containing a 10x10 matrix of observations $Y$. 
The matrix represents values on a grid where the row index $i \in \{0, 1, ..., 9\}$ corresponds to the feature $X_1$, and the column index $j \in \{0, 1, ..., 9\}$ corresponds to the feature $X_2$.

You need to fit the following non-linear model to this data:
$Y = \theta_1 X_1^2 + \theta_2 X_2^2$

To understand the robustness of your fit for $\theta_1$, you must compute the 95% bootstrap confidence interval. 

Write a C++ program (`/home/user/fit_model.cpp`) that performs the following steps:
1. **Multi-dimensional Data Parsing**: Read `/home/user/data.txt` into a 2D array structure, then flatten it into 100 distinct observation tuples $(X_1, X_2, Y)$.
2. **Bootstrapping**: Perform $B=1000$ bootstrap iterations. In each iteration, create a bootstrap sample by drawing $100$ observations from your flattened data *with replacement*. 
   *Constraint:* Use `std::mt19937` initialized with the seed `42`, and `std::uniform_int_distribution<int>(0, 99)` to select indices.
3. **Optimization**: For *each* bootstrap sample, use Gradient Descent to find the parameters $\theta_1$ and $\theta_2$ that minimize the Mean Squared Error (MSE): $\frac{1}{N} \sum (Y - \hat{Y})^2$.
   *Hyperparameters:* Initialize $\theta_1 = 0.0$ and $\theta_2 = 0.0$. Use a learning rate of `0.00001` and exactly `1000` iterations per gradient descent run.
4. **Confidence Interval**: Collect the 1000 fitted values for $\theta_1$. Sort them in ascending order. The lower bound of the 95% CI is the value at index 25, and the upper bound is the value at index 974.

Compile and run your C++ program. Your program must write a single file `/home/user/result.txt` containing exactly three space-separated floating-point numbers:
`Mean_Theta1 CI_Lower CI_Upper`
(Where `Mean_Theta1` is the average of the 1000 bootstrap estimates for $\theta_1$).