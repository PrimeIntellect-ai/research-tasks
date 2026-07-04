You are a data analyst working for a retail company. You have been given a dataset of user purchase ratings, but the data is messy and needs to be cleaned, transformed, and analyzed to generate basic product recommendations.

Your task is to process the data and generate outputs according to the following specifications:

**Data Location:** `/home/user/data/purchases.csv`
**Columns:** `user_id,item_id,rating`

**Phase 1: ETL & Outlier Handling**
1. Read the `purchases.csv` file.
2. Filter out any rows where the `rating` is missing (empty), less than `1.0`, or greater than `5.0`.
3. Identify "bot" or "outlier" users: any `user_id` that has strictly more than `5` valid purchases (after step 2) is considered an outlier. Remove all rows associated with these outlier users.
4. Save the resulting cleaned dataset (with header) to `/home/user/output/cleaned.csv`.

**Phase 2: Sampling / Bootstrap**
1. Generate a bootstrap sample (sampling *with replacement*) of exactly `500` rows from the data rows of `cleaned.csv` (excluding the header). 
2. Save this sample (with the original header included at the top) to `/home/user/output/bootstrap.csv`.

**Phase 3: Similarity Search & Recommendation**
1. Using the `cleaned.csv` dataset, compute the item-item co-occurrence count. Co-occurrence is defined as the number of unique users who have purchased both Item A and Item B.
2. Find the top 3 items most frequently co-purchased with `ITEM_001`. (Exclude `ITEM_001` itself from the recommendations).
3. If there is a tie in co-occurrence counts, resolve it by sorting the `item_id` in ascending alphabetical order.
4. Save the top 3 recommendations to `/home/user/output/recommendations.csv` with the header `recommended_item_id,co_occurrence_count`.

You may use any language (Python, Bash, awk, etc.) to complete this task. 
Ensure the output directory `/home/user/output/` exists before writing files.