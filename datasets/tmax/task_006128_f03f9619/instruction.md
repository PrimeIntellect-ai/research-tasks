You are an ML engineer preparing training data to test a new similarity search model. You need to create a small test suite by taking a specific sample of "anchor" embeddings, joining them with their vector data, and finding their nearest neighbors in a "candidate" embedding set.

Your task is to write a C program that performs this multi-source join and similarity search.

You are provided with three files in your home directory `/home/user/`:
1. `anchors.csv`: Contains anchor IDs and their 3D vector representations. Format: `id,x,y,z` (where id is an integer, and x, y, z are floats).
2. `candidates.csv`: Contains candidate IDs and their 3D vector representations. Format: `id,x,y,z`.
3. `sample_ids.txt`: Contains a subsample of anchor IDs (one integer per line) that we want to process for our test set.

Write a C program located at `/home/user/match_samples.c` that does the following:
1. Reads the IDs from `sample_ids.txt`.
2. Looks up the corresponding vector data for each sampled ID from `anchors.csv`.
3. For each sampled anchor vector, searches `candidates.csv` to find the candidate with the minimum Euclidean distance. (If there is a tie in distance, pick the candidate with the strictly smaller integer ID).
4. Outputs the matches to a file named `/home/user/matches.csv`. The output format must be `anchor_id,closest_candidate_id` with one match per line, in the exact order the anchor IDs appear in `sample_ids.txt`.

Once written, compile your program using standard `gcc` (e.g., `gcc -O2 /home/user/match_samples.c -o /home/user/match_samples -lm`) and run it to produce `/home/user/matches.csv`.

Ensure your program handles missing or malformed data gracefully (though you can assume the provided test files will be well-formatted CSVs).