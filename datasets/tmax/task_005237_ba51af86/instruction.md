You are a Machine Learning Engineer preparing a training dataset and baseline recommendations using a probabilistic approach. 

You have a dataset of user interactions with various items in `/home/user/data/events.csv`. 
The file contains the following columns: `user_id`, `item_id`, `clicks`, `views`.

Your task is to write a Python script that performs the following pipeline and outputs a specific JSON file:

**Phase 1: Feature Engineering & Bayesian Smoothing**
Due to data sparsity, simple Click-Through Rates (CTR = clicks/views) are unreliable for items with few views. Calculate a smoothed CTR for every (user, item) pair using Bayesian inference with a Beta-Binomial conjugate prior.
Assume a fixed global prior of $\alpha_0 = 2.0$ and $\beta_0 = 8.0$.
The Smoothed CTR for a specific user-item pair is calculated as:
`smoothed_ctr = (clicks + 2.0) / (views + 2.0 + 8.0)`

Create a User-Item feature matrix where rows are `user_id`s (sorted numerically), columns are `item_id`s (sorted numerically), and the values are the `smoothed_ctr`. If a user has no events for an item, assume `clicks = 0` and `views = 0` for that pair when calculating the smoothed CTR.

**Phase 2: Similarity Search**
For every user in the dataset, find their nearest neighbor (the most similar user) based on the Euclidean distance between their `smoothed_ctr` vectors in the User-Item matrix. If there is a tie, pick the user with the smaller `user_id`. A user cannot be their own nearest neighbor.

**Phase 3: Recommendation**
For each user, recommend exactly one item based on their nearest neighbor's preferences. The recommended item should be the item with the highest `smoothed_ctr` for the *neighbor*, restricted only to items that the *target user* has 0 views on. If there is a tie for the highest smoothed CTR, pick the item with the smaller `item_id`. If the target user has already viewed all items the neighbor has viewed, output `null` for the recommendation.

**Output Configuration:**
Write the final results to `/home/user/recommendations.json`.
The format must be a JSON dictionary mapping the target `user_id` (as a string) to a dictionary containing `nearest_neighbor` (integer) and `recommended_item` (integer or null).

Example format:
```json
{
  "1": {
    "nearest_neighbor": 3,
    "recommended_item": 5
  },
  "2": {
    "nearest_neighbor": 1,
    "recommended_item": null
  }
}
```

Ensure your Python script creates this file exactly as specified. You may use standard Python libraries, `pandas`, `numpy`, or `scikit-learn` (install them if needed).