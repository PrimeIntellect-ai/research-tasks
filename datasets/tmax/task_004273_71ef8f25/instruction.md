You are a data engineer responsible for a mathematical ETL pipeline that processes physics simulation data, fits a regression model, and generates diagnostic plots. 

Your predecessor left a broken pipeline. You have two files in your home directory: `/home/user/generate_data.py` (which generates the raw simulation data) and `/home/user/pipeline.py` (the main ETL and modeling script). 

Currently, the pipeline has two major issues:
1. **Mathematical/ETL Bug:** The regression model's accuracy is extremely poor (Mean Absolute Error > 1000). The simulation features have vastly different numerical scales, which is completely breaking the `Ridge` regression model. You need to fix the ETL process in `pipeline.py` to properly scale the features before training the model. 
2. **Diagnostic Plot Bug:** The script is supposed to save a diagnostic plot to `/home/user/residuals.png`, but the resulting image is completely blank (white). You need to identify and fix the backend/plotting misconfiguration in `pipeline.py` that is causing the blank plot.

Your task is to:
1. Fix `pipeline.py` so that the `Ridge` regression achieves an MAE of **less than 50.0**.
2. Fix the plotting logic in `pipeline.py` so `/home/user/residuals.png` contains the actual scatter plot, not a blank canvas.
3. Make the script output the final test MAE as a JSON object to `/home/user/metrics.json` in this exact format: `{"mae": 45.123}`.
4. Create a reproducible entrypoint bash script at `/home/user/run_pipeline.sh` that:
   - Creates a Python virtual environment at `/home/user/venv`.
   - Activates it and installs required packages (`numpy`, `pandas`, `scikit-learn`, `matplotlib`).
   - Runs `python /home/user/generate_data.py` to create `data.csv`.
   - Runs `python /home/user/pipeline.py`.

Ensure `run_pipeline.sh` is executable (`chmod +x`). Do not modify `generate_data.py`.