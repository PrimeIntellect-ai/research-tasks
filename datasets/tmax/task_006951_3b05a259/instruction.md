You are an AI assistant helping a machine learning engineer prepare training labels for a spectroscopic analysis model. 

We have a raw spectroscopic signal file located at `/home/user/raw_signal.csv`. The file has a header `wavelength,intensity`. The signal models an absorption spectrum with a baseline of 1.0 and two Gaussian absorption dips. 

Unfortunately, the instrument's numerical integration diverged at high wavelengths, causing massive, erroneous oscillations at `wavelength > 800`.

Your task:
1. Read the dataset and filter out all data points where `wavelength > 800` to remove the divergence artifact.
2. Fit the remaining data to a double-Gaussian absorption model:
   `I(x) = 1.0 - A1 * exp(-(x - mu1)^2 / (2 * sigma1^2)) - A2 * exp(-(x - mu2)^2 / (2 * sigma2^2))`
   Assume `mu1 < mu2`.
3. Using the fitted parameters, computationally solve for the `wavelength` (x) between `mu1` and `mu2` where the two individual absorption components are equal. That is, where `A1 * exp(-(x - mu1)^2 / (2 * sigma1^2)) == A2 * exp(-(x - mu2)^2 / (2 * sigma2^2))`.
4. Output a JSON file at `/home/user/labels.json` containing the fitted means and the intersection point.

The JSON should have exactly this structure:
```json
{
  "mu1": <float>,
  "mu2": <float>,
  "intersection_x": <float>
}
```

Constraints:
- You must write a Python script to perform the data processing, curve fitting, and equation solving.
- Do not use external libraries other than `numpy`, `scipy`, `pandas`, and standard Python libraries.
- The values in the JSON should be accurate to at least 2 decimal places.

Execute your script to produce `/home/user/labels.json`.