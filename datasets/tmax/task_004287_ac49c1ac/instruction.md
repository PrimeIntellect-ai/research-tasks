You are an MLOps engineer debugging a Bash-based audio processing and embedding pipeline. We have an experiment directory at `/app/experiment/` containing a raw audio recording of an interview (`/app/experiment/interview.wav`). 

There is an existing pipeline script at `/home/user/pipeline.sh` that splits the audio into 10-second segments, normalizes their volume, transcribes them using our local CLI tool (`/app/tools/transcribe`), and extracts text embeddings using (`/app/tools/text2vec`). The pipeline splits the segments into a "train" set (first 80% of segments) and a "test" set (remaining 20%).

However, there is a critical "data leak" in the pipeline: the script computes the peak volume for normalization using the *entire* `interview.wav` file before splitting it. Because our transcription model is extremely sensitive to volume distribution, this global normalization artificially inflates the accuracy on the test set, masking real-world performance where test audio volume parameters are unknown.

Your task is to refactor `/home/user/pipeline.sh` strictly using Bash and standard CLI tools (`ffmpeg`, `awk`, `bc`, etc.) to:
1. Split the raw audio into 10-second segments first.
2. Separate the segments into train (first 80%) and test (last 20%) numerically based on their timestamps.
3. Compute the maximum volume (`max_volume`) **only** from the train segments.
4. Apply this specific `max_volume` gain factor to normalize both the train and test segments independently.
5. Run the transcription and embedding tools on the properly normalized test segments.
6. Calculate the average cosine similarity of the test embeddings against the ground truth embeddings (already stored in `/app/experiment/ground_truth/`).

Output your final test set average cosine similarity score to a file named `/home/user/metrics.txt` in the format: `Test_Similarity: <score>`.

Your refactored pipeline must be reproducible and must execute successfully when run via `bash /home/user/pipeline.sh`. The final score will be evaluated against a programmatic threshold.