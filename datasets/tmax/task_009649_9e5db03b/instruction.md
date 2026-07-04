You are a performance engineer tasked with debugging a model training pipeline that is failing to converge. 

A background training job is currently running on the system, but another engineer accidentally deleted its primary log file (`/home/user/app/training.log`). The process is still running and holds the file open. 

Your task is to:
1. **Recover the deleted log**: Find the deleted log file that is still held open by the running `runner.py` process. Save its current contents to `/home/user/app/recovered.log`.
2. **Reconstruct the timeline**: Analyze `/home/user/app/recovered.log` alongside the existing system log at `/home/user/app/system.log`. Find the exact timestamp (in the format `YYYY-MM-DD HH:MM:SS`) when the training loss first strictly exceeded `100.0`. Write only this timestamp to `/home/user/app/divergence_time.txt`.
3. **Fix the convergence failure**: The training algorithm in `/home/user/app/train.py` implements a simple gradient descent, but it diverges instead of converging. Identify and fix the mathematical/algorithmic bug in the weight update step. 
4. **Add assertion validation**: Add a Python assertion in the training loop of `/home/user/app/train.py` to ensure the loss is never negative (`assert loss >= 0.0, "Loss cannot be negative"`).
5. **Verify**: Run the fixed `/home/user/app/train.py` script. It will print a final converged value. Redirect this standard output to `/home/user/app/success.txt`.

Constraints:
- Do not kill the background `runner.py` process until you have recovered the log.
- All files must be placed exactly at the paths specified.