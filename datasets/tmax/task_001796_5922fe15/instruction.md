You are a data analyst working on an A/B testing experiment. You have two datasets:
- `/home/user/experiments.csv`: Contains `user_id`, `group` ('A' or 'B'), `conversion` (0 or 1), and `session_duration` (float).
- `/home/user/feedback.csv`: Contains `user_id` and `feedback_text` (string).

Your task is to analyze these datasets and write the results to `/home/user/results.json`.

Follow these exact steps:
1. **Data Joining:** Join the two datasets on `user_id`.
2. **Bootstrap CI:** Estimate the 95% confidence interval for the difference in mean `session_duration` between Group B and Group A (i.e., Mean_B - Mean_A). 
   - Use the percentile method (2.5th and 97.5th percentiles).
   - Perform exactly 1000 bootstrap iterations.
   - For each iteration, sample with replacement from Group A's durations (size = len(A)) and Group B's durations (size = len(B)). 
   - Set `numpy.random.seed(42)` immediately before your bootstrap loop, and use `numpy.random.choice` for sampling.
3. **Bayesian Inference:** Calculate the posterior mean for the conversion rate of Group B.
   - Assume a Beta prior distribution with parameters $\alpha = 1, \beta = 1$.
   - The posterior mean formula is $(\alpha + \text{successes}) / (\alpha + \beta + \text{total trials})$.
4. **Embedding & Retrieval:** Filter the joined dataset to only include users in Group B who converted (`conversion == 1`).
   - Use `scikit-learn`'s `TfidfVectorizer` (with default parameters) to compute embeddings for their `feedback_text`. Fit the vectorizer ONLY on these users' feedback texts.
   - Transform the query string `"fast checkout"` using the fitted vectorizer.
   - Compute the cosine similarity between the query and the feedback embeddings to find the `user_id` with the highest similarity score. In case of a tie, pick the first one.
5. **Experiment Tracking Plot:** There is a broken script at `/home/user/plot.py` that is supposed to plot the bootstrap distribution. Due to a backend misconfiguration and incorrect matplotlib API usage, it produces a blank image. Fix the script so that when you run it, it correctly saves a non-blank histogram to `/home/user/bootstrap_plot.png`.

Output your analysis results to `/home/user/results.json` in the following format:
```json
{
  "ci_lower": 1.2345,
  "ci_upper": 4.5678,
  "posterior_mean": 0.550,
  "most_similar_user_id": 42
}
```
Round `ci_lower`, `ci_upper`, and `posterior_mean` to 4 decimal places. The `most_similar_user_id` should be an integer.