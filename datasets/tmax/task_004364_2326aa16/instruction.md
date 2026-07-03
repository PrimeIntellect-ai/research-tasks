You are an AI assistant helping a data researcher organize a growing repository of datasets. The researcher has extracted metadata tags from various datasets but needs to automatically categorize them and find similar datasets within the new categories.

Your task is to write a C program that performs Bayesian classification and similarity matching on this metadata.

You will find two input files in `/home/user/`:
1. `model.txt`: Contains the parameters for a Naïve Bayes classifier. 
   - The first line contains the prior probabilities for Category 0 and Category 1, formatted as: `PRIOR <prob_0> <prob_1>`
   - The subsequent lines contain the conditional probabilities of specific integer tags given each category, formatted as: `TAG <tag_id> <prob_given_0> <prob_given_1>`
   *(Note: For any tag not listed in `model.txt`, assume a default probability of 0.5 for both categories).*

2. `datasets.txt`: Contains the dataset metadata. 
   - Each line represents one dataset.
   - The format is: `Dataset_ID Tag1 Tag2 ... TagN`
   - IDs and Tags are integers. There can be up to 10 tags per dataset.

Write a C program named `/home/user/organizer.c` that does the following:
1. **Bayesian Inference**: For each dataset, calculate the unnormalized posterior probability for Category 0 and Category 1 using Naïve Bayes. 
   Formula for Category $C$: 
   $Score(C) = P(C) \times \prod_{t \in tags} P(t | C)$
   Assign each dataset to the category with the strictly greater score. If $Score(0) = Score(1)$, default to Category 0.
   
2. **Similarity Search**: For each dataset, find the *most similar* dataset that has been assigned to the *same category*. 
   - Similarity is defined as the Jaccard Index: $|A \cap B| / |A \cup B|$, where A and B are the sets of tags for the two datasets.
   - Do not compare a dataset to itself. 
   - If there is a tie in maximum Jaccard Index among multiple candidates, select the one with the lowest `Dataset_ID`.
   - If there are no other datasets in the assigned category, output `-1` for the most similar ID and `0.00` for the score.

3. **Output**: Your program must write the results to `/home/user/output.csv` with the following format for each dataset (sorted by `Dataset_ID` in ascending order):
   `Dataset_ID,Assigned_Category,Most_Similar_Dataset_ID,Jaccard_Index`
   
   Format `Jaccard_Index` to exactly two decimal places (e.g., `0.33`, `1.00`).

Compile your program using `gcc /home/user/organizer.c -o /home/user/organizer -O2` and run it to produce the output file.