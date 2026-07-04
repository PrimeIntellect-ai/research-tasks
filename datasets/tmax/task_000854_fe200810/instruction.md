You are a developer tasked with debugging a failing machine learning build pipeline.

The project is located in `/home/user/build_system/`.
When you run the build script `python train.py`, it fails with a convergence error (the loss becomes `NaN`).

Your tasks are:
1. Analyze the codebase to understand why the gradient descent training loop is failing to converge.
2. Identify the bug in the data transformation/preprocessing step that causes this convergence failure. 
3. Fix the bug in `train.py` so that the model successfully trains and the build passes. 

Requirements:
- Do not change the learning rate, the random seed, the number of epochs, or the model architecture.
- Fix the logic error in the data preprocessing step.
- When fixed, running `python train.py` will succeed, print "Build passed!", and generate a `weights.npy` file.

You can use any debugging techniques you prefer (printing, interactive debugger, etc.).