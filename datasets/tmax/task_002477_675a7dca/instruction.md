You are an MLOps engineer tasked with analyzing experiment artifacts. You have been given a set of experiment metadata logs and corresponding model architecture embeddings.

Your task is to build a lightweight ETL and analysis pipeline to extract insights from these artifacts. 

The data is located in `/home/user/experiments/`:
1. `metadata.jsonl`: Contains JSON lines with keys `experiment_id`, `learning_rate`, `batch_size`, and `accuracy`.
2. `embeddings.csv`: Contains comma-separated values with columns `experiment_id`, `v1`, `v2`, `v3` representing the 3-dimensional embedding of the model architecture.

Write a script (Python is recommended, but you may use any standard shell tools) to compute the following:
1. **Most Similar Models:** Calculate the cosine similarity between all pairs of model embeddings. Identify the pair of `experiment_id`s that have the highest cosine similarity (excluding an experiment's similarity to itself).
2. **Hyperparameter Correlation:** Calculate the Pearson correlation coefficient between `learning_rate` and `accuracy` across all experiments in the metadata file.

Once computed, output your results to a file at `/home/user/report.json` with the exact following structure:
```json
{
  "most_similar_pair": ["<exp_id_1>", "<exp_id_2>"],
  "lr_acc_correlation": <float_rounded_to_4_decimal_places>
}
```
*Note: The `most_similar_pair` array must have the two experiment IDs sorted alphabetically.*