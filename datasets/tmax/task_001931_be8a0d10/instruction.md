You are a data scientist analyzing 1D emission spectroscopy data. We need to evaluate how much the spectral intensity deviates from a uniform background noise model across different regions of our spatial domain.

Write a Go program (save it as `/home/user/analyze.go` and run it) that processes the raw spectral data and calculates the deviation. 

Here are the precise steps your Go program must follow:

1. **Read Data:** Read the spatial spectroscopy data from `/home/user/spectra.csv`. The file has a header `x,intensity`. The `x` values are integers from `0` to `99`. 
2. **Signal Processing (Smoothing):** Apply a 3-point moving average filter to the `intensity` values to reduce noise. 
   - For an internal point $i$, the smoothed value is $y'_i = (y_{i-1} + y_i + y_{i+1}) / 3$.
   - For the first point ($i=0$), use a 2-point average: $y'_0 = (y_0 + y_1) / 2$.
   - For the last point ($i=99$), use a 2-point average: $y'_{99} = (y_{98} + y_{99}) / 2$.
3. **Domain Decomposition:** Split the spatial domain into two disjoint sub-domains based on the `x` coordinate:
   - **Domain A**: $x < 50$
   - **Domain B**: $x \ge 50$
4. **Probability Normalization:** For each sub-domain separately, normalize the *smoothed* intensity values so that they sum to exactly `1.0`. Treat these normalized arrays as discrete probability distributions $P_A$ and $P_B$.
5. **Distribution Distance Metric:** We want to measure how far these empirical distributions diverge from a theoretical uniform distribution $Q$. 
   - For Domain A, let $Q_A$ be a uniform distribution where every point has probability $1 / N_A$ (where $N_A$ is the number of points in Domain A).
   - For Domain B, let $Q_B$ be a uniform distribution where every point has probability $1 / N_B$.
   - Calculate the Kullback-Leibler (KL) Divergence for both domains: $D_{KL}(P || Q) = \sum_{i} P_i \ln(P_i / Q_i)$, using the natural logarithm.
6. **Output:** Output the two KL divergence values as a JSON object saved to `/home/user/fit_results.json`. The file must have exactly this structure:
```json
{
  "kl_domain_a": <float>,
  "kl_domain_b": <float>
}
```

Ensure your Go program is completely self-contained, using only standard library packages. Compile and execute your program to produce the final JSON file.