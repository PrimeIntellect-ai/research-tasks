You are a data analyst tasked with evaluating the results of an A/B test for an e-commerce platform.

You have been provided with an event log file located at `/home/user/events.csv`. This file contains the following columns:
- `user_id`: A unique identifier for each user.
- `event_type`: The type of event (`view`, `click`, or `purchase`).
- `value`: The monetary value associated with the event (only non-zero for `purchase` events).
- `group`: The experimental group the user belongs to (`A` for Control, `B` for Variant). Every user belongs to exactly one group.

Your objective is to determine if there is a statistically significant difference in the *total purchase value per user* between Group A and Group B.

Please perform the following steps:
1. **Transform and Aggregate**: Calculate the total purchase value for each user. Note that if a user has no `purchase` events (e.g., they only have `view` or `click` events), their total purchase value should be evaluated as `0`.
2. **Hypothesis Testing**: Conduct a two-sided Welch's t-test (independent two-sample t-test with unequal variances) comparing the total purchase values of users in Group A versus users in Group B. Use the `scipy.stats` module.
3. **Reporting**: Write the test results to a JSON file at `/home/user/ab_test_results.json`. The JSON file must strictly follow this format:
   ```json
   {
       "t_statistic": <float>,
       "p_value": <float>
   }
   ```
   *Requirement*: Round both the `t_statistic` and `p_value` to exactly 4 decimal places.

Ensure that all processing is done using Python, and you may install any necessary data science libraries (e.g., pandas, scipy) using `pip`.