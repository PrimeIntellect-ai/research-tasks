You are assisting a machine learning engineer in preparing training data for a contrastive learning model. The model requires "hard negatives" – samples that are highly similar to a target sample but not the exact same sample.

We have a dataset of 3D item embeddings in a CSV file located at `/home/user/data/embeddings.csv`.

Your task is to:
1. Write a C program at `/home/user/compute_negatives.c` that reads the embeddings and computes the dot product similarity between all pairs.
2. The C program MUST use the OpenBLAS library (`cblas_ddot`) to perform the dot product calculations. You will need to install the necessary development packages and configure your compilation command to link against it.
3. For each item (by `id`), find the *single* other item (different `id`) that has the highest dot product score. 
4. The C program must output these pairs to `/home/user/data/hard_negatives.csv` with the header `id,hard_negative_id,score`. The `score` must be printed to exactly 4 decimal places. The rows should be ordered by the original `id` ascending.
5. Create a shell script at `/home/user/track_experiment.sh` that:
   - Compiles the C program.
   - Runs the C program.
   - Uses standard Linux command-line tools (like `awk`) to calculate the average of the `score` column from `hard_negatives.csv`.
   - Appends a line exactly in the format `[Experiment CL-01] AvgScore=<avg_score_to_4_decimal_places>` to the file `/home/user/experiment.log`.

The input CSV (`/home/user/data/embeddings.csv`) has the following structure (with a header):
`id,v1,v2,v3`

Make sure all directories exist, install any necessary dependencies, and ensure your final script (`track_experiment.sh`) is executable and works end-to-end.