You are a support engineer responding to a developer's urgent ticket. They are trying to run a machine learning training pipeline, but it is failing in multiple ways. They provided you access to their repository located at `/home/user/ml_project`.

Here are the issues reported and the steps you must take to resolve them:

1. **Authentication Misconfiguration & Git Forensics**: The script `train_model.py` requires a database password to be set as the `DB_PASSWORD` environment variable. The developer forgot the password, but they mentioned it was accidentally hardcoded in an early git commit before being removed. 
   - Search the git history of `/home/user/ml_project` to recover the deleted password string.
   - Save this exact password string into a new file at `/home/user/db_secret.txt`.
   - Export it as the `DB_PASSWORD` environment variable in your shell so the script can authenticate.

2. **Query Result Debugging**: The training data is loaded from `/home/user/ml_project/data.db`. The developer noted that a sensor malfunction caused several rows in the database to have a corrupted `target` value of `-999.0`. 
   - Inspect `train_model.py` and modify the SQL query so that it actively ignores/excludes any rows where the `target` column equals `-999.0`.

3. **Convergence Failure Repair**: When the developer ran the script, the model failed to converge (the loss exploded to infinity/NaN). 
   - Debug the simple gradient descent implementation in `train_model.py`. 
   - The learning rate (`lr`) is currently configured too high. Change the learning rate to `0.01` to allow the model to converge.

4. **Run Diagnostics**: Once the script is fixed, run `python3 /home/user/ml_project/train_model.py`. The script is programmed to automatically write the final training loss to `/home/user/diagnostics.log` upon a successful, converged run.

Ensure that by the end of your session, `db_secret.txt` contains the correct password, `train_model.py` is patched, and `diagnostics.log` contains the final calculated loss.