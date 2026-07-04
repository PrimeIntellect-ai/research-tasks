You are an AI assistant helping a computational researcher run an optimization simulation pipeline. 

The researcher has a black-box simulation script located at `/home/user/sim.sh`. This script takes two continuous parameters, `X` and `Y`, and outputs a simulated yield metric `Z` (a floating-point number).

Your task is to build a fully reproducible computation pipeline in Bash that performs a grid search optimization to find the parameters that maximize `Z`, reshapes the observational data, and generates a visualization.

Specifically, write a single Bash script at `/home/user/pipeline.sh` that does the following when executed:
1. **Grid Search Optimization**: Iterate over `X` from `0.0` to `5.0` (inclusive) with a step size of `0.5`, and `Y` from `0.0` to `5.0` (inclusive) with a step size of `0.5`. For each combination, execute `/home/user/sim.sh X Y` to get the `Z` value.
2. **Find the Optimum**: Track the maximum `Z` value and its corresponding `X` and `Y`. Save this to `/home/user/best_params.txt` in exactly this format: `X=<x>, Y=<y>, Z=<z>` (e.g., `X=1.5, Y=2.0, Z=42.50`).
3. **Observational Data Reshaping**: Save the evaluated `Z` values into a 2D matrix format in `/home/user/grid_data.txt`. The file should have exactly 11 rows and 11 columns. Rows should correspond to the `Y` values (from 0.0 at the top row to 5.0 at the bottom row), and columns should correspond to the `X` values (from 0.0 at the left column to 5.0 at the right column). Values should be space-separated.
4. **Experimental Data Visualization**: Generate a Gnuplot script at `/home/user/plot.gp` that reads `/home/user/grid_data.txt` and creates a heatmap (image matrix) saved as a PNG file at `/home/user/heatmap.png`. The Bash script should execute this Gnuplot script as its final step.

Constraints:
- You must use Bash as the primary language for your pipeline script. You may rely on standard Unix tools like `awk`, `bc`, `seq`, etc., to handle multi-dimensional logic and floating-point math.
- Do not modify `/home/user/sim.sh`.
- The pipeline script must be executable and run non-interactively.