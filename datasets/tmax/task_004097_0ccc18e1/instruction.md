You are a data engineer building a new ETL pipeline for a recommendation engine. We need to process user interaction logs to extract user preferences using a Bayesian model, calculate item similarities, and ensure the pipeline is completely reproducible regardless of data ingestion order.

Please build this pipeline in Rust. 

**Setup**
There is a raw log file located at `/home/user/clicks.csv` with the following columns: `user_id,item_id,category,clicked`. `clicked` is `1` if the user clicked the item, and `0` if they saw it but did not click.

**Step 1: The Rust ETL Pipeline**
Initialize a new Rust project at `/home/user/etl_pipeline`.
Write a Rust program that reads `/home/user/clicks.csv` and computes two things:
1. **Bayesian User Profiles**: For each user and category combination, calculate the posterior Beta distribution parameters representing their preference. Assume a uniform prior Beta distribution ($\alpha=1$, $\beta=1$). Every `clicked=1` is a success (adds to $\alpha$), and `clicked=0` is a failure (adds to $\beta$).
2. **Item Similarities**: Compute the Jaccard similarity between all unique pairs of items. An item's "set" for Jaccard similarity is the set of `user_id`s that have `clicked=1` on that item. Ignore users with `clicked=0` for this calculation. Ensure you only compute for $item_1 < item_2$ (lexicographically) to avoid duplicates. Jaccard similarity is $|A \cap B| / |A \cup B|$.

Output the results to `/home/user/output.json` with the following exact structure:
```json
{
  "user_profiles": [
    {"user_id": "u1", "category": "A", "alpha": 2, "beta": 2}
  ],
  "item_similarities": [
    {"item_1": "i1", "item_2": "i2", "jaccard": 0.3333}
  ]
}
```
*Constraints for output.json:*
- Round the `jaccard` similarity to 4 decimal places.
- Sort the `user_profiles` list first by `user_id`, then by `category` (ascending strings).
- Sort the `item_similarities` list first by `item_1`, then by `item_2` (ascending strings).

**Step 2: Pipeline Reproducibility Testing**
Data engineers must guarantee that shuffling input logs does not affect the aggregated results.
Write a bash script at `/home/user/test_reproducibility.sh` that does the following:
1. Creates two shuffled versions of `/home/user/clicks.csv` (keep the header intact, but shuffle the data rows randomly).
2. Runs your Rust ETL pipeline on the first shuffled file, saving the output to `out1.json`.
3. Runs your Rust ETL pipeline on the second shuffled file, saving the output to `out2.json`.
4. Compares `out1.json` and `out2.json`. If they are exactly identical, write the word `REPRODUCIBLE` to `/home/user/repro_status.txt`. Otherwise, write `FAILED`.

Run the reproducibility test so that `/home/user/repro_status.txt` is created. Also run the pipeline on the original `/home/user/clicks.csv` to generate the final `/home/user/output.json`.