You are a Machine Learning Engineer preparing training data for a new recommendation system. The data stream has been contaminated with poisoned user profiles designed to artificially inflate the recommendation scores of certain target items.

Your goal is to build a robust C++ data sanitization pipeline that filters out these malicious profiles.

You have been provided with a proprietary, stripped similarity oracle located at `/app/sim_oracle`. This binary takes two file paths as command-line arguments (e.g., `/app/sim_oracle profileA.json profileB.json`) and outputs a similarity score between them. You do not have the source code for this binary.

To help you calibrate your filter, you have been provided with:
1. A reference clean profile at `/home/user/reference.json`.
2. A directory of known clean profiles at `/home/user/sample_clean/`.
3. A directory of known malicious profiles at `/home/user/sample_evil/`.

**Your objectives:**
1. **Analysis Environment Setup:** Set up your C++ environment and any necessary tools to script interactions with the `/app/sim_oracle` binary.
2. **Hypothesis Testing:** Write an analysis script (you may use Python/R for this exploratory step) to evaluate the similarity scores of the files in `sample_clean` and `sample_evil` against `reference.json`. Perform a statistical hypothesis test (e.g., Welch's t-test) to find a statistically rigorous threshold that separates the distributions with at least 99.9% confidence.
3. **C++ Implementation:** Implement the final data sanitization filter in C++. Create a file `/home/user/filter_data.cpp` and compile it to an executable named `/home/user/filter_data`.
   
   Your C++ executable must have the following CLI signature:
   `/home/user/filter_data <input_directory> <output_directory>`
   
   For every file in the `<input_directory>`, your program should invoke the `/app/sim_oracle` comparing the file to `/home/user/reference.json`. If the similarity score indicates the file is clean based on your derived threshold, copy the file to the `<output_directory>`. If it is malicious, simply ignore it.

**Constraints:**
- Your final program must be compiled and ready to run at `/home/user/filter_data`.
- Do not hardcode the names of the files in the input directory. Your program should iterate over all files present in the given `<input_directory>`.