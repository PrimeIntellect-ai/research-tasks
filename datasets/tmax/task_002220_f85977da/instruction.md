You are a Data Scientist tasked with cleaning and analyzing a dataset on a locked-down production server. The catch? The Python and R runtimes are currently broken, and you do not have root access to install them or their packages. You must perform the entire data processing pipeline using only standard Linux shell tools (Bash, awk, sed, grep, bc, coreutils, etc.).

Your workspace is `/home/user/`.
You have been provided with a raw dataset at `/home/user/raw_data.csv`.
The file is a comma-separated values (CSV) file with a header row. 
The columns are: `ID`, `Feature_A`, `Feature_B`, `Feature_C`, `Target`.

Your task involves three phases:

**Phase 1: Feature Engineering (Min-Max Scaling)**
1. Read `/home/user/raw_data.csv`.
2. Apply Min-Max scaling to `Feature_A`, `Feature_B`, and `Feature_C`. 
   The formula is: `Scaled_Value = (Value - Min) / (Max - Min)`
3. Output the result to `/home/user/engineered.csv`.
4. The output must be a CSV with the header: `ID,Norm_A,Norm_B,Norm_C,Target`.
5. All normalized values must be formatted to exactly 4 decimal places (e.g., `0.0000`, `1.0000`, `0.4567`). The `Target` column remains an integer.

**Phase 2: Correlation Analysis**
1. Using the data in `/home/user/engineered.csv`, calculate the Pearson correlation coefficient between each normalized feature (`Norm_A`, `Norm_B`, `Norm_C`) and the `Target`.
2. Output the results to `/home/user/correlations.txt`.
3. The format of the file must be exactly three lines, like this (rounded to 4 decimal places):
   ```
   Norm_A: 0.1234
   Norm_B: -0.5678
   Norm_C: 0.9012
   ```

**Phase 3: Similarity Search**
1. Using the features in `/home/user/engineered.csv` (Norm_A, Norm_B, Norm_C), calculate the Euclidean distance between the row with ID `REF_001` and all other rows. Do not include `Target` in the distance calculation.
2. Find the top 3 most similar rows to `REF_001` (i.e., the 3 rows with the smallest Euclidean distance to `REF_001`, excluding `REF_001` itself).
3. If there is a tie in distance, break it by sorting the tied IDs alphabetically.
4. Output *only the IDs* of these 3 rows, one per line, ordered from most similar (smallest distance) to least similar, to `/home/user/similar.txt`.

Ensure all calculations maintain high precision internally before rounding the final outputs to 4 decimal places.