You are an MLOps engineer tasked with analyzing an experiment tracking database. One of our recent training runs failed, and we want to estimate what its final accuracy would have been by looking at similar historical experiments. 

You have a log file located at `/home/user/logs.jsonl` containing JSON Lines. Each line represents an experiment and contains the following keys:
- `exp_id`: String identifier
- `description`: Text notes on the architecture and optimizer
- `learning_rate`: Float
- `batch_size`: Integer
- `accuracy`: Float (final metric)

Your task is to build a simple ETL and similarity search pipeline in Python to find the top 2 successful experiments most similar to the failed one (`exp_id` = "exp_failed") and average their accuracies.

Follow these specific feature engineering and linear algebra steps to represent each experiment as a 7-dimensional vector:
1. Tokenize the `description` by converting it to lowercase and splitting by spaces.
2. Create a 5-dimensional Bag-of-Words (term frequency) vector for the exact vocabulary: `["resnet", "adam", "sgd", "dropout", "cnn"]`. Each dimension should be the count of how many times that exact word appears in the description.
3. Append a 6th dimension for the learning rate, scaled: `learning_rate * 1000.0`.
4. Append a 7th dimension for the batch size, scaled: `batch_size / 10.0`.
*(This creates a single 7-dimensional vector per experiment).*

Calculate the **Cosine Similarity** between the vector for "exp_failed" and the vectors of all other experiments. 

Find the 2 experiments with the highest cosine similarity to "exp_failed" (excluding "exp_failed" itself). Calculate the mean `accuracy` of these 2 experiments.

Write your final result to `/home/user/recommendation.txt` in exactly this format:
`Mean Accuracy: <value>` (where `<value>` is rounded to 3 decimal places, e.g., 0.865).