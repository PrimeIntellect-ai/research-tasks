You are an AI assistant helping a researcher organize and process experimental datasets. The researcher has two datasets containing sensor readings and metadata. You need to write a C program to join these datasets, clean the data (handle missing values and outliers), perform a similarity search to find the most similar experiments, and output the result.

Here is the setup:
The data files are located in `/home/user/data/`:
1. `/home/user/data/metadata.csv`: Contains `ExpID,Category`. 
2. `/home/user/data/series.csv`: Contains 5 consecutive sensor readings per experiment in the format `ExpID,V1,V2,V3,V4,V5`. Some values are missing (represented by empty fields between commas, e.g., `E02,1.0,,3.0,4.0,5.0`). 

Write a C program (e.g., saved as `/home/user/process.c`) and compile/run it to perform the following steps:
1. **Multi-source joining:** Filter the data to only include experiments that exist in *both* files AND have the Category set to `Target` in the metadata.
2. **Outlier handling:** For the sensor readings of the valid experiments, cap any value greater than `100.0` to `100.0`, and any value less than `0.0` to `0.0`. Do this *before* calculating the mean for missing values.
3. **Missing value handling:** Replace any missing values (empty strings) with the arithmetic mean of the *present, capped* values for that specific experiment. (Assume every row has at least one valid reading).
4. **Similarity search:** Calculate the Euclidean distance between the cleaned 5-dimensional reading vectors for all pairs of valid `Target` experiments.
5. **Output:** Find the single pair of experiments with the smallest Euclidean distance. 

Write the most similar pair and their distance to `/home/user/closest_pair.txt` in the exact following format:
`ExpA,ExpB,Distance`

**Formatting rules:**
- `ExpA` must be lexicographically smaller than `ExpB` (e.g., `E01,E04`, not `E04,E01`).
- `Distance` must be formatted to exactly 4 decimal places (e.g., `2.8284`).
- Ensure the output file contains exactly one line.

Please write the C code, compile it using `gcc`, and execute it to generate the final `/home/user/closest_pair.txt` file.