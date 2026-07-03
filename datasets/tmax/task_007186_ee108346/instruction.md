You are a data analyst tasked with evaluating an A/B test for a recent marketing campaign. You have been provided with a daily conversions dataset in `/home/user/campaign_data.csv`.

The dataset has the following columns: `date,variant,visitors,conversions`.
Unfortunately, the data ingestion pipeline had some glitches. Some rows contain negative values for `visitors` (due to tracking errors) and should be completely ignored.

Your task is to build a reproducible data processing pipeline using Bash and Go to clean the data and perform a Bayesian analysis.

Step 1: Data Cleaning
Write a bash script or command that filters out any rows in `/home/user/campaign_data.csv` where `visitors` is less than or equal to 0, or where `conversions` is negative. Skip the CSV header when doing calculations, but ensure your intermediate or processed data is handled correctly. 

Step 2: Aggregation and Bayesian Inference (Go)
Write a Go program `/home/user/analyze.go` that reads the cleaned data and aggregates the total `visitors` and total `conversions` for each variant (A and B).
Using a Beta(1, 1) prior for the conversion rate of each variant, calculate the parameters of the posterior Beta distribution ($\alpha$ and $\beta$).
Recall that for a Beta prior $\text{Beta}(\alpha_0, \beta_0)$ and binomial data with $k$ successes (conversions) out of $n$ trials (visitors), the posterior is $\text{Beta}(\alpha_0 + k, \beta_0 + n - k)$.

For both variants A and B, calculate:
1. The posterior mean conversion rate: $\mu = \frac{\alpha}{\alpha + \beta}$
2. The posterior variance: $\sigma^2 = \frac{\alpha \beta}{(\alpha + \beta)^2 (\alpha + \beta + 1)}$
3. A 95% credible interval approximation using the normal approximation: $[\mu - 1.96\sigma, \mu + 1.96\sigma]$

Step 3: Output Formatting
Your Go program must output the final results to a JSON file at `/home/user/results.json` with the following exact structure, rounding all float values to exactly 4 decimal places:

```json
{
  "A": {
    "mean": 0.0000,
    "variance": 0.0000,
    "ci_lower": 0.0000,
    "ci_upper": 0.0000
  },
  "B": {
    "mean": 0.0000,
    "variance": 0.0000,
    "ci_lower": 0.0000,
    "ci_upper": 0.0000
  }
}
```

Make sure to compile and run your Go program so that `/home/user/results.json` is generated.