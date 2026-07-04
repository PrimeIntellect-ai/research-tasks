You are assisting a machine learning engineer who is preparing a training dataset for a sequence classification model. Previously, the data pipeline produced non-reproducible feature vectors due to floating-point values being aggregated in arbitrary, non-deterministic orders. 

To fix this, we need to rebuild the feature extraction step using standard, deterministic Bash text-processing utilities (like `grep`, `awk`, `sort`, etc.).

You have been provided with a raw data file at `/home/user/raw_alignments.tsv`. 
It is a tab-separated file with three columns: `AlignmentID`, `TargetSeq`, and `Score` (a floating-point number).

Your task is to create a processed dataset at `/home/user/curated_features.tsv` following these exact rules:
1. Filter the dataset to include only rows where the `TargetSeq` starts with the exact DNA primer motif `GATTACA`.
2. Group the filtered rows by the **length** of the `TargetSeq`.
3. For each group (each unique sequence length), count the number of matching sequences.
4. To ensure deterministic floating-point behavior downstream, gather all the `Score` values for each group, **sort them numerically in descending order**, and join them with commas into a single string.
5. Write the results to `/home/user/curated_features.tsv` as a tab-separated file with the following columns: `SequenceLength`, `MatchCount`, `SortedScores`.
6. The final output file must be sorted numerically in ascending order by `SequenceLength`.

Example output format for `/home/user/curated_features.tsv`:
```
8	1	0.55
10	3	3.41,2.10,1.25
12	2	9.99,0.01
```

Use only standard Linux command-line tools. Do not write a Python or Perl script. Ensure the output file is created exactly at `/home/user/curated_features.tsv`.