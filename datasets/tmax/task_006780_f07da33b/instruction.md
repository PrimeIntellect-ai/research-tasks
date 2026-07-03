You are acting as a computational physics researcher studying the thermal distribution of an anharmonic oscillator. 

Your goal is to write and execute a Python script that characterizes a specific non-Gaussian probability distribution by combining numerical integration, nonlinear equation solving, numerical differentiation, and probability distance metrics.

The unnormalized probability density function of the particle's position $x$ is given by:
`w(x; c) = exp(-c * x^2 - x^4)`
defined on the domain $x \in [-5, 5]$. 

Here are the precise steps you must implement in a script to solve this problem:

1. **Discretization and Integration:**
   Create a linearly spaced grid of exactly `10,000` points for $x \in [-5, 5]$ (inclusive of endpoints). All integrals in this task must be approximated using the **composite trapezoidal rule** (`scipy.integrate.trapezoid` or `numpy.trapz`) over this exact discrete grid.
   The normalized PDF is $P(x; c) = w(x; c) / Z(c)$, where $Z(c) = \int_{-5}^{5} w(x; c) dx$.
   The variance of the distribution is $V(c) = \int_{-5}^{5} x^2 P(x; c) dx$.

2. **Nonlinear Equation Solving:**
   We need to find the specific parameter $c^*$ such that the variance $V(c^*) = 0.25$. 
   Solve this nonlinear equation to find $c^*$ within the bracket $c \in [0.0, 5.0]$. Use a tolerance of at least `1e-6`.

3. **Numerical Differentiation:**
   Once you have found $c^*$, compute the first derivative of the variance with respect to $c$ at $c^*$, i.e., $V'(c^*)$. 
   Use the central finite difference method with a step size of $h = 10^{-4}$:
   $V'(c^*) \approx \frac{V(c^* + h) - V(c^* - h)}{2h}$.

4. **Probability Distribution Distance:**
   Compare the non-Gaussian distribution $P(x; c^*)$ to a pure Gaussian distribution $Q(x)$ that has mean 0 and the same variance (0.25). 
   Let $p_i = P(x_i; c^*)$ and $q_i = \frac{1}{\sqrt{2\pi(0.25)}} \exp(-\frac{x_i^2}{2(0.25)})$ evaluated on your grid.
   Normalize both discrete distributions over the grid such that their sums equal 1: $\hat{p}_i = p_i / \sum p_i$ and $\hat{q}_i = q_i / \sum q_i$.
   Calculate the Kullback-Leibler (KL) divergence from $\hat{q}$ to $\hat{p}$:
   $D_{KL}(\hat{p} \parallel \hat{q}) = \sum_{i} \hat{p}_i \ln\left(\frac{\hat{p}_i}{\hat{q}_i}\right)$.

5. **Output Requirement:**
   Save your final results to a JSON file located at `/home/user/results.json`. The JSON file must have exactly these keys and the calculated numerical values (as floats):
   - `"c_star"`: The calculated value of $c^*$.
   - `"variance_derivative"`: The calculated numerical derivative $V'(c^*)$.
   - `"kl_divergence"`: The calculated KL divergence $D_{KL}(\hat{p} \parallel \hat{q})$.

You may use standard scientific Python libraries (`numpy`, `scipy`). Write, run, and debug your code in the terminal to produce the required output file.