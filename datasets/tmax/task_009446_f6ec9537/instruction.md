You are helping a data science researcher organize their experimental datasets and fix a broken analysis pipeline. The researcher has raw tabular data, but their current workflow is manual, the visualization step is producing blank plots due to a headless server environment misconfiguration, and there is no tracking of experiment metrics.

You need to build a reproducible pipeline using a `Makefile` and Python scripts.

Here is the current state and your objectives:
1. **Raw Data:** You have a dataset at `/home/user/dataset/sensors.csv`. It contains 1000 rows. The columns are `sensor_type` (categorical) and `reading_1` through `reading_20` (numerical floats).
2. **Tabular Transformation:** Create a script `/home/user/scripts/aggregate.py` that reads the raw dataset, groups the data by `sensor_type`, and calculates the mean for all 20 numerical readings. Save this aggregated data to `/home/user/dataset/aggregated.csv`.
3. **Dimensionality Reduction & Fix Plotting:** There is an existing script at `/home/user/scripts/pca_plot.py` that is *supposed* to read `aggregated.csv`, perform PCA to reduce the 20 features down to 2 components, and save a scatter plot. However, it currently produces a completely blank or corrupted image because it was written for a desktop environment and fails in our headless server (backend misconfiguration). 
   - Fix `/home/user/scripts/pca_plot.py` so it properly generates and saves the plot to `/home/user/results/pca_plot.png` without requiring an X11/display server.
4. **Experiment Tracking:** Modify the PCA step so that it calculates the sum of the `explained_variance_ratio_` for the 2 PCA components. Save this metric to a JSON file at `/home/user/results/metrics.json` in the exact format: `{"explained_variance_sum": <float>}`.
5. **Reproducible Pipeline:** Create a `/home/user/Makefile`. The default `all` target should execute the aggregation script, then the PCA/plotting script, ensuring all output directories exist and outputs are generated in the correct order. The `Makefile` should also have a `clean` target that removes `aggregated.csv`, `pca_plot.png`, and `metrics.json`.

Ensure all output files are placed exactly as specified. Do not use absolute paths in the Makefile in a way that breaks if executed from `/home/user`.