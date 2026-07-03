You are acting as a data analyst. We have an old, undocumented, stripped binary located at `/app/legacy_recommender` that we use to generate daily product recommendations from CSV exports. We need to deprecate this black-box binary and replace it with an open-source, readable implementation.

Your task is to write a bash script (using standard tools like `awk`, `join`, `sort`, etc.) that replicates the exact behavior of the binary bit-for-bit.

Here is what we know about the pipeline:
1. The binary accepts two arguments: the path to a ratings CSV and the path to an items CSV.
   Usage: `/app/legacy_recommender <ratings.csv> <items.csv>`
2. `items.csv` has no header and the format: `ItemID,Feature1,Feature2` (all positive integers).
3. `ratings.csv` has no header and the format: `UserID,ItemID,Rating` (all positive integers).
4. The binary processes these files to build a simple "user profile" and then recommends exactly **one** new item per user using a similarity search (a dot product). 
5. It prints the output to stdout in the format: `UserID,RecommendedItemID`, sorted numerically by UserID.
6. The recommendation must be an item the user has **not** rated yet in the `ratings.csv` file.

To succeed, you must track your experiments against the binary. Create your own test data files, run them through `/app/legacy_recommender`, and deduce the exact numerical logic (e.g., how the user profile is weighted by ratings, how ties are broken). 

Write your final solution to `/home/user/recommender.sh`.
It must take the exact same arguments and produce identical standard output.
You can assume standard GNU utilities (awk, sed, bash, etc.) are available. 

Constraints:
- The script must be written primarily in Bash/AWK.
- Ensure your script gracefully handles users who have rated all available items (they should not be printed in the output).
- Ensure your output perfectly matches the binary's output for any arbitrary valid CSV inputs.