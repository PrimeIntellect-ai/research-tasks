You are tasked with resolving data corruption issues caused by a malfunctioning configuration manager ETL pipeline. A recent bug caused the job to retry excessively, producing duplicate records. Additionally, some network timeouts resulted in missing data points. 

You have been provided with a raw metrics file at `/home/user/raw_metrics.csv`. The file is in a "long" format with the following columns: `ts` (integer timestamp), `server` (string), `metric` (string), and `value` (float).

Perform the following data processing steps using Python:
1. **Deduplication:** Read the CSV. Identify duplicate records based on the combination of `ts`, `server`, and `metric`. Keep only the *last* occurring record for any such combination, discarding earlier duplicates.
2. **Reshaping:** Convert the dataset from long format to a "wide" format. The resulting format should have `ts` and `server` as the index/identifying columns, and each unique `metric` (e.g., `cpu`, `mem`, `disk`) as its own column containing the respective values.
3. **Imputation:** Sort the data by `ts` ascending. Group by `server` and handle missing metric values. First, apply linear interpolation to fill gaps. If there are still missing values at the beginning or end of a server's timeline, use backward filling (bfill) then forward filling (ffill).
4. **Similarity Computation:** Compute the time-averaged profile for each server. This means calculating the mean of each metric across all timestamps for each server.
5. **Distance Calculation:** Using the averaged metric profiles, calculate the Euclidean distance between all distinct pairs of servers. 
6. **Output:** Identify the pair of servers that have the most similar configuration profiles (i.e., the smallest Euclidean distance). Write this result to `/home/user/closest_servers.json` in the exact format below:

```json
{
  "server1": "A",
  "server2": "B",
  "distance": 1.2345
}
```
*Note: `server1` must be alphabetically before `server2`. Round the `distance` to exactly 4 decimal places.*