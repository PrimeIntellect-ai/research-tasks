I am a researcher organizing a dataset of research paper abstracts. I need you to write a Go program that acts as a simple inference engine to classify new papers, recommend similar existing papers, and benchmark its own performance.

You will find two datasets:
- `/home/user/data/train.csv`: The existing classified dataset. (Columns: `id`, `category`, `abstract`)
- `/home/user/data/test.csv`: The new unclassified dataset. (Columns: `id`, `category`, `abstract`)

Write a Go program at `/home/user/organizer.go` that does the following:

1. **Preprocessing**: 
   - Parse both CSV files.
   - Tokenize the `abstract` text for each paper: convert to lowercase, remove all commas (`,`) and periods (`.`), and split by spaces into a set of unique words.

2. **Similarity Search & Classification Model (K-Nearest Neighbors)**:
   - For a given test paper, compute the Jaccard Similarity between its unique word set and the unique word sets of all training papers. 
   - Jaccard Similarity = (Size of Intersection of sets) / (Size of Union of sets).
   - Find the top K=3 most similar training papers (resolve ties by choosing the smaller training `id`).
   - **Classification**: Assign the category that appears most frequently among the top K=3 neighbors. If there's a tie in category frequency, pick the category of the neighbor with the absolute highest similarity score among the tied categories.
   - **Recommendation**: Record the IDs of the top 3 most similar training papers.

3. **Inference Benchmarking & Experiment Tracking**:
   - Measure the exact time taken to run the similarity search and classification for all test papers combined.
   - Compute `throughput_qps` (queries per second) = `Total test papers / Total time in seconds`.
   - Calculate `accuracy` = `Number of correctly classified test papers / Total test papers`.
   - Append a JSON object to `/home/user/experiment_log.jsonl` with the format:
     `{"k": 3, "accuracy": 0.XX, "throughput_qps": Y.YY}`

4. **Recommendation Output**:
   - Write a CSV file to `/home/user/recommendations.csv` containing the recommendations for the test set. 
   - The header must be: `test_id,sim_1,sim_2,sim_3`
   - Each row should have the test paper's ID followed by the IDs of its top 3 most similar training papers, ordered from most similar to 3rd most similar.

Finally, execute your Go program to generate `/home/user/recommendations.csv` and the entry in `/home/user/experiment_log.jsonl`.