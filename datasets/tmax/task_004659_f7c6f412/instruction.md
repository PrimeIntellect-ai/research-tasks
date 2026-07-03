You are a data analyst working with video analytics. We have a video of an experiment located at `/app/experiment.mp4` and a pre-computed CSV of frame embeddings at `/app/embeddings.csv`. The CSV has headers: `frame_id,emb_0,emb_1,...,emb_127` representing a 128-dimensional embedding for each frame. The `frame_id` is a 0-indexed integer corresponding to the video frames.

Your task is to create a robust query tool at `/home/user/query_tool` (which must be an executable script or binary) that processes queries for similarity search, hypothesis testing, and correlation analysis. 

The tool must accept exactly two command-line arguments: a target frame index `F` and an integer `K`:
`./query_tool <F> <K>`

Your tool must perform the following steps:
1. Validate `F`. If `F` is not present in the CSV, print exactly `{"error": "invalid F"}` to standard output and exit with code 0.
2. Retrieve the 128-dimensional embedding for frame `F`.
3. Compute the cosine similarity between frame `F`'s embedding and *all* frames in the CSV (including `F` itself).
4. Sort all frames by cosine similarity in descending order. If there is a tie in similarity (rounded to 6 decimal places), resolve it by sorting `frame_id` in ascending order.
5. Select the top `K` frames from this sorted list.
6. Calculate the Pearson correlation coefficient between the `frame_id`s and their corresponding `cosine similarity` for these top `K` frames. (Use sample standard deviation. If the standard deviation of either array is 0, return `0.0`).
7. Calculate the 95% confidence interval for the mean cosine similarity of these top `K` frames. Use a standard Z-score of `1.96` for the calculation: `Margin of Error = 1.96 * (sample_std_dev / sqrt(K))`.
8. Extract these exact `K` frames from `/app/experiment.mp4`. Compute the average brightness across all these `K` frames. To do this, extract the frames as RGB images, and calculate the mean value of all pixels across all color channels (R, G, B) for all `K` frames combined. (Do not use grayscale conversion, just the raw mean of all RGB values).
9. Print a single JSON object to standard output with exactly these keys and precise types (floats rounded to 4 decimal places):
```json
{
  "f": 10,
  "k": 5,
  "top_frames": [10, 15, 8, 22, 1],
  "correlation": 0.1234,
  "mean_similarity": 0.8500,
  "ci_lower": 0.8100,
  "ci_upper": 0.8900,
  "avg_brightness": 105.4321
}
```

The automated system will fuzz-test your executable against a reference oracle implementation with dozens of random `(F, K)` pairs to ensure bit-exact equivalence of the JSON output. Performance matters, so optimize your script. Make sure `/home/user/query_tool` is executable. You may use Python, C++, or any standard language available in a typical Linux environment.