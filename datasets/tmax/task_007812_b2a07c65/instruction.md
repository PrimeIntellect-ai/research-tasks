You are an analyst at a digital marketing agency evaluating the true conversion rates of several ad campaigns using a Bayesian approach. You have two datasets located in your home directory:

1. `/home/user/clicks.csv` - Contains `campaign_id`, `platform`, and `clicks`.
2. `/home/user/conversions.csv` - Contains `campaign_id` and `conversions`.

Your task is to write and execute a Python script that does the following:
1. Load and join both datasets on `campaign_id`.
2. Filter out any campaigns that have strictly fewer than 100 `clicks`.
3. We model the conversion rate $\theta$ for each campaign using a Beta-Binomial conjugate model. Assume a common prior of Beta($\alpha=2$, $\beta=10$) for all campaigns.
4. For each retained campaign, calculate the posterior Beta distribution parameters ($\alpha_{post}$ and $\beta_{post}$). Remember that for $k$ conversions out of $n$ clicks, $\alpha_{post} = \alpha + k$ and $\beta_{post} = \beta + n - k$.
5. Compute the posterior mean of the conversion rate.
6. Compute the 95% Equal-Tailed Credible Interval (the 2.5th and 97.5th percentiles of the posterior distribution).
7. Save the results to `/home/user/campaign_posteriors.csv`. 

The output CSV must have exactly these columns in this order:
`campaign_id`, `posterior_mean`, `lower_95`, `upper_95`

Format requirements:
- Sort the output CSV by `campaign_id` in ascending alphabetical order.
- Round `posterior_mean`, `lower_95`, and `upper_95` to exactly 4 decimal places (e.g., 0.1450).
- Do not include the index in the output CSV.

You may use standard data science libraries like `pandas` and `scipy`.