You are an MLOps engineer tasked with managing a large-scale data storage cluster that has recently been polluted with poisoned experiment artifacts. We need to automatically filter out these poisoned files before they corrupt our downstream pipelines.

We have a proprietary, stripped binary located at `/app/artifact_embedder`. This tool analyzes an artifact file and outputs a 5-dimensional numerical embedding (space-separated floats) representing the file's structural properties. 

You have been provided with a small training dataset:
- `/home/user/data/train_clean/` contains examples of valid, clean artifacts.
- `/home/user/data/train_evil/` contains examples of poisoned artifacts.

Your task is to write a Bash script at `/home/user/classifier.sh` that acts as a filter.
Requirements:
1. The script must take exactly one argument: the absolute path to an artifact file.
2. It must execute `/app/artifact_embedder <file>` to obtain the file's embedding.
3. It must use Bash-native tools (e.g., `awk`, `bc`) to implement a classification model (such as Naive Bayes, or nearest-centroid based on Euclidean distance) to determine if the file is clean or poisoned, using the patterns you discover from the training data.
4. If the script classifies the file as **clean**, it must exit with status code `0`.
5. If the script classifies the file as **poisoned**, it must exit with status code `1`.

You are expected to first analyze the training data to compute your model parameters (like cluster centroids or probability distributions) and hardcode or dynamically load them into your script.

Your script will be automatically evaluated against a hidden, larger test suite of clean and poisoned artifacts. It must achieve 100% accuracy on this hidden test set.