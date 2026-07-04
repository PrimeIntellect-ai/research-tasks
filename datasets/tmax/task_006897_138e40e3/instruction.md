You are an MLOps engineer tasked with tracking experiment artifacts for a minimal C++ ML pipeline. 

Your evaluation script `/home/user/evaluate.cpp` computes a 1D embedding (feature) for text data, performs hyperparameter tuning (grid search) for a simple threshold-based binary classifier, and writes the results to an artifact file. However, analogous to a plotting script saving a blank image due to a backend misconfiguration, your script currently produces an empty artifact file (`report.txt`). Additionally, the feature extraction logic is incomplete.

Your task:
1. Fix the bug in `/home/user/evaluate.cpp` that causes `report.txt` to be completely empty or fail to write.
2. Complete the `compute_feature(const std::string& text)` function in the script. It must calculate and return the ratio of vowels (`a`, `e`, `i`, `o`, `u`, case-insensitive) to the total number of characters in the text. (If the string is empty, return 0.0).
3. Compile the script using `g++ -std=c++14 evaluate.cpp -o evaluate`.
4. Run `./evaluate`.

Ensure that after running the executable, `/home/user/report.txt` is successfully created and contains the printed best threshold and accuracy. Do not change the grid search logic, the dataset, or the output formatting in the script—only fix the file writing bug and implement the feature calculation.