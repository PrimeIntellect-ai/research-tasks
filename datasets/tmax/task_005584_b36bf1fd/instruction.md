You are an MLOps engineer responsible for evaluating experiment artifacts. We have run an A/B test on two models to determine which has a higher success rate. The results are stored in a CSV file at `/home/user/eval_results.csv` with the following format:

```csv
model_id,trials,successes
model_A,500,410
model_B,500,425
```

Your task is to calculate the posterior probability that Model B is better than Model A (i.e., the true success rate of Model B is strictly greater than the true success rate of Model A). 

Perform the following steps:
1. Model the success rate of each model using a Beta-Binomial conjugate model. Assume a uniform `Beta(1, 1)` prior for both models.
2. Install any necessary mathematical or scientific libraries you need (e.g., `scipy` for Python). You may use Python, R, or any standard CLI tools available.
3. Calculate the exact probability $P(\theta_B > \theta_A)$ using numerical integration or an exact mathematical formulation to ensure numerical accuracy. Do not use low-sample Monte Carlo simulations, as the result must be highly accurate.
4. Save the calculated probability, rounded to exactly 4 decimal places, to `/home/user/prob.txt`.
5. Implement a decision rule: If the probability is greater than `0.9500`, write the word `DEPLOY` to `/home/user/decision.txt`. Otherwise, write `RETAIN` to `/home/user/decision.txt`.

Ensure all your scripts and commands are executed and the final text files contain only the required output.