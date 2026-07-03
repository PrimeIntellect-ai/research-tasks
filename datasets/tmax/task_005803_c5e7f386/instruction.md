You are a data scientist tasked with fitting a custom probability distribution to empirical data and comparing it to a baseline distribution.

You have a dataset of observations located at `/home/user/samples.csv` (a single column of numerical values).

Perform the following steps using Python:
1. Load the data from `/home/user/samples.csv`.
2. Compute the normalized empirical probability density (histogram) of the samples using exactly 50 bins within the range `[-5, 5]`. Use the bin centers as your $x$-coordinates and the normalized frequencies (density) as your $y$-coordinates.
3. You need to fit a custom Probability Density Function (PDF) of the form:
   $$f(x; a, b) = \frac{1}{Z(a,b)} \exp(-a x^2 - b x^4)$$
   where the normalization constant $Z(a,b)$ is given by the numerical integration:
   $$Z(a,b) = \int_{-5}^{5} \exp(-a t^2 - b t^4) dt$$
4. Use `scipy.optimize.curve_fit` to fit $f(x; a, b)$ to your histogram data (using the bin centers and densities) to find the optimal parameters $a$ and $b$. Use an initial guess of `a = 1.0` and `b = 0.1`.
5. Once you have the optimal parameters $a_{opt}$ and $b_{opt}$, calculate the $L_2$ distance between your fitted custom PDF and the standard normal distribution $\mathcal{N}(0, 1) = \frac{1}{\sqrt{2\pi}} \exp(-x^2/2)$ over the interval `[-5, 5]`. 
   The $L_2$ distance is defined as:
   $$L_2 = \sqrt{ \int_{-5}^{5} \left( f(x; a_{opt}, b_{opt}) - \mathcal{N}(x; 0, 1) \right)^2 dx }$$
   Use numerical integration (e.g., `scipy.integrate.quad`) to compute this.
6. Save the final optimized parameters and the calculated $L_2$ distance into a JSON file at `/home/user/results.json`. The JSON file must have the keys `"a"`, `"b"`, and `"L2_distance"`. Round each value to exactly 4 decimal places.

Ensure that all calculations use standard `numpy` and `scipy` functions.