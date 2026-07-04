You are a data scientist analyzing star detection data from a recent telescope observation. 

We have recorded the spatial coordinates of detected photon events in a $100 \times 100$ field of view (where $x \in [0, 100]$ and $y \in [0, 100]$). The data is stored in an HDF5 file located at `/home/user/star_data.h5`, which contains two datasets: `x` and `y` (1D numpy arrays of the same length).

The events are theorized to be a mixture of uniform background noise and a single star cluster. The star cluster's spatial distribution is modeled as a 2D isotropic Gaussian. 

The overall Probability Density Function (PDF) for an event at $(x, y)$ is:
$P(x, y) = w \cdot \frac{1}{2\pi\sigma^2} \exp\left( -\frac{(x-\mu_x)^2 + (y-\mu_y)^2}{2\sigma^2} \right) + (1-w) \cdot \frac{1}{10000}$

Where:
- $\mu_x, \mu_y$ are the center coordinates of the star cluster.
- $\sigma$ is the spatial spread of the cluster.
- $w$ is the mixing weight (the fraction of events belonging to the cluster).
- $\frac{1}{10000}$ is the uniform density over the $100 \times 100$ field.

Your task is to:
1. Read the `x` and `y` datasets from `/home/user/star_data.h5`.
2. Construct the Negative Log-Likelihood (NLL) function for this mixture model.
3. Use a continuous optimization algorithm (e.g., `scipy.optimize.minimize`) to find the Maximum Likelihood Estimates (MLE) for the parameters: $\mu_x$, $\mu_y$, $\sigma$, and $w$. 
   - Note: Enforce logical bounds during optimization (e.g., $0 \le w \le 1$, $\sigma > 0$, and $\mu_x, \mu_y \in [0, 100]$).
4. Save your fitted parameters to a JSON file at `/home/user/cluster_params.json` with the exact keys: `"mu_x"`, `"mu_y"`, `"sigma"`, and `"w"`. Round the values to 3 decimal places.

Your solution will be evaluated by calculating the Negative Log-Likelihood of your parameters on the dataset. You must find the global minimum (or extremely close to it).