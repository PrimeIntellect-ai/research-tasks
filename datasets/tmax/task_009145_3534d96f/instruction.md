You are a data scientist working on a pure Bash-based data processing pipeline. You've inherited a directory `/home/user/data_pipeline` containing a raw dataset and a broken script used for similarity search and recommendation.

The pipeline is supposed to:
1. Parse a CSV file `/home/user/data_pipeline/vectors.csv` containing item IDs and their 3-dimensional feature vectors.
2. Given a target Item ID, compute the Manhattan distance between the target item and all other items using `awk`.
3. Sort the results and output the top 2 closest item IDs (excluding the target itself) to a specified output file.

However, the current script `/home/user/data_pipeline/recommend.sh` is buggy:
- It fails to compute the absolute differences correctly (incorrect numerical configuration/logic for distance).
- It doesn't sort the distances numerically, causing lexicographical sorting bugs.
- It doesn't correctly exclude the target item from the recommendations.

Your task:
1. Fix the script `/home/user/data_pipeline/recommend.sh`. The script takes two arguments: the target ID and the path to the output file.
   Usage: `./recommend.sh <target_id> <output_file>`
2. Run the script for the target ID `target_1` and save the recommendations to `/home/user/data_pipeline/top2_recommendations.txt`.

The output file `/home/user/data_pipeline/top2_recommendations.txt` should contain exactly two lines, each with the ID of the recommended item. Do not include the distance values in the final output file, only the item IDs, ordered from closest to furthest.