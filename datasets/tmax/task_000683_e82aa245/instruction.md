You are a data analyst working for an e-commerce company. We have run an A/B test on two marketing campaigns ('Alpha' and 'Beta') and collected daily performance data.

Your task is to write a Python script at `/home/user/analyze.py` that processes the raw daily data and performs a Bayesian analysis to determine which campaign is better.

The input data is located at `/home/user/campaign_data.csv` and has the following columns:
`date,campaign_id,clicks,conversions`

Your script must perform the following steps:
1. Read the CSV file and aggregate the total `clicks` and `conversions` for each `campaign_id` ('Alpha' and 'Beta') across all dates.
2. We assume the conversion rate follows a Binomial likelihood with a Beta distribution prior. Using an uninformative **Beta(1, 1)** prior, calculate the Bayesian posterior mean of the conversion rate for both campaigns. 
   *(Hint: The posterior distribution will be Beta(conversions + 1, clicks - conversions + 1))*
3. Estimate the probability that Campaign Alpha's true conversion rate is strictly greater than Campaign Beta's true conversion rate. To do this:
   - Use Monte Carlo sampling.
   - Set `numpy.random.seed(42)` exactly once, immediately before generating samples.
   - Draw exactly 1,000,000 samples from Campaign Alpha's posterior distribution using `numpy.random.beta`.
   - Then, draw exactly 1,000,000 samples from Campaign Beta's posterior distribution using `numpy.random.beta`.
   - Calculate the fraction of samples where Alpha's sampled rate is greater than Beta's sampled rate.
4. Save the results as a JSON file at `/home/user/report.json` with the following exact structure (round all floats to 5 decimal places):

```json
{
  "Alpha": {
    "clicks": 123,
    "conversions": 12,
    "posterior_mean": 0.10400
  },
  "Beta": {
    "clicks": 145,
    "conversions": 15,
    "posterior_mean": 0.10884
  },
  "prob_alpha_greater_beta": 0.43210
}
```

Make sure to execute your script so that `/home/user/report.json` is generated.