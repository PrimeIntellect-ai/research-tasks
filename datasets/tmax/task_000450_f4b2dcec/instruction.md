You are tasked with debugging a failing build in a distributed machine learning pipeline. The build currently fails during integration testing because our custom parameter updater, `optimizer.py`, suffers from numerical instability, causing convergence failures (specifically, it frequently outputs `NaN` values due to exploding gradients and division-by-zero errors).

Here is what you need to do:
1. **Analyze the Logs:** The logs from the failing build are scattered across three services in `/app/build_logs/`: `compute_node.log`, `param_server.log`, and `validator.log`. You must reconstruct the timeline of the failing request to find the developer's diagnostic notes logged just before the crash. These notes describe the exact algorithmic changes (e.g., gradient clipping and an epsilon stabilizer) needed to fix the convergence issue.
2. **Extract Hyperparameters:** The exact numerical values for the clipping threshold and the epsilon stabilizer were lost during a recent repository migration. However, a screenshot of a Slack message containing these values was preserved at `/app/slack_snippet.png`. You will need to extract these values from the image.
3. **Fix the Optimizer:** The buggy script is located at `/home/user/build/optimizer.py`. You must rewrite its `update_weights` function to incorporate the clipping and stabilization logic extracted from the logs and the image. 

**Script Interface Specifications:**
- Your script (`/home/user/build/optimizer.py`) must accept two arguments: `--weights` and `--gradients`. 
- Both arguments will be passed as JSON-formatted strings representing lists of floating-point numbers of equal length.
- The script must print a single JSON-formatted string representing the list of updated weights to standard output, and nothing else.
- The learning rate (`lr`) is fixed at `0.01`.

To verify your fix, an automated system will extensively test your `optimizer.py` against a pre-compiled, correct reference binary (`/app/oracle_optimizer`) using randomized inputs. Your script's output must perfectly match the oracle's output for all inputs.