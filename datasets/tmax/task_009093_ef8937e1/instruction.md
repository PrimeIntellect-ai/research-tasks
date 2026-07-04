You are a data analyst working on a product recommendation system. You have been given a dataset of 5-dimensional product embeddings in a CSV file located at `/home/user/data.csv`. 

A former colleague wrote a C++ script, `/home/user/recommender.cpp`, to perform similarity search. Given a target product ID, the script is supposed to find the top 3 most similar products based on cosine similarity of their embeddings. However, the project was left unfinished and has two major issues:

1. **Missing Dependency**: The script relies on the `Eigen` library (Eigen3) for vector operations, but it is not installed on the system. You do not have root (`sudo`) access to install it via the package manager. You must download or clone the Eigen headers locally to `/home/user/eigen` and compile the script against them.
2. **Blank/Zero Output Bug**: Even when compiled, the script fails to produce meaningful similarities. The previous analyst mentioned that the similarities always compute to `0` or `NaN` because of a data-type misconfiguration that rounds all floating-point embedding values down to zero during parsing. Similar to how a misconfigured matplotlib backend produces blank plots, this misconfigured data type produces "blank" similarity scores.

Your task is to:
1. Download the Eigen library to `/home/user/eigen` (e.g., using `wget https://gitlab.com/libeigen/eigen/-/archive/3.4.0/eigen-3.4.0.tar.gz` and extracting it).
2. Fix the logical bug(s) in `/home/user/recommender.cpp` so that it correctly reads the floating-point values from the CSV and accurately computes the cosine similarity.
3. Compile the fixed script into an executable named `/home/user/recommender`.
4. Run the executable to find the top 3 recommendations for Target ID `10`.
5. The C++ script is already written to output the results. Ensure it writes the final recommendations to `/home/user/output.txt` in the exact format: `TargetID: SimID1, SimID2, SimID3` (ordered from most similar to least similar).

Ensure your final compiled program correctly executes and writes the expected `/home/user/output.txt`.