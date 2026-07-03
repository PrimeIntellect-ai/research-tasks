You are an MLOps engineer tasked with tracking and evaluating experiment artifacts. We have a set of historical experiment configurations and their outcomes, and we need to predict the outcomes of a new set of experiments based on their similarity to past ones. 

To do this efficiently, we use a custom CLI tool called `vmath` to compute distances between experiment artifact vectors. The source code for `vmath` (version 1.2) is vendored at `/app/vmath-1.2`. However, the previous engineer left it in a broken state, and it currently fails to compile.

Your tasks are as follows:

1. **Fix and Build `vmath`**: Navigate to `/app/vmath-1.2`. Identify and fix the compilation issue (hint: it's a missing linker flag in the Makefile for the math library). Compile the tool so that the executable `vmath` is generated in that directory. The tool takes two comma-separated vectors as arguments and prints their Euclidean distance (e.g., `./vmath 1.0,2.0 3.0,4.0`).

2. **Data Preparation**: You have two datasets in `/home/user/data`:
   - `historical.csv`: Contains past experiments. Format: `experiment_id,feat1,feat2,feat3,feat4,outcome_class`
   - `new_experiments.csv`: Contains new experiments to evaluate. Format: `experiment_id,feat1,feat2,feat3,feat4`
   Both files have a header row.

3. **Classification via Similarity**: Using ONLY Bash shell scripts and standard coreutils (e.g., `awk`, `join`, `sort`), write a script `/home/user/evaluate.sh` that does the following:
   - Iterates over each experiment in `new_experiments.csv`.
   - Uses your compiled `/app/vmath-1.2/vmath` to calculate the distance between the new experiment's feature vector and every feature vector in `historical.csv`.
   - Finds the single closest historical experiment (1-Nearest Neighbor).
   - Assigns the `outcome_class` of that closest historical experiment to the new experiment.

4. **Output Generation**: Your script must output the predictions to `/home/user/predictions.csv`. The output file must have the header `experiment_id,predicted_class` followed by the predicted rows.

Run your script to generate `/home/user/predictions.csv`. An automated evaluator will check the accuracy of your predictions against the true outcomes. You must achieve an accuracy of at least 95%.