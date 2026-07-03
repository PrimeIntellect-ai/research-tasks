As a performance engineer, you have been tasked with optimizing a critical bioinformatics script used for primer design. The script `/home/user/primer_tool.py` attempts to find the optimal melting temperature and GC ratio to maximize a simulated sequence alignment score. 

Currently, the tool uses a custom, incredibly slow gradient descent implementation that acts as a major bottleneck. Your goals are:

1. Profile the original script using Python's built-in `cProfile` module and save the text output to `/home/user/profile_baseline.txt`.
2. Modify `/home/user/primer_tool.py`. Remove the custom `custom_gradient_descent` logic in the `optimize()` function and replace it with Scipy's Nelder-Mead simplex algorithm (`scipy.optimize.minimize` with `method='Nelder-Mead'`). 
3. The objective function `evaluate_primer_loss` takes an array `[temperature, gc_ratio]`. The initial guess should remain `[50.0, 0.3]`.
4. Ensure that the existing scientific regression tests pass by running `pytest /home/user/test_primer.py`. These tests verify both the mathematical correctness of your optimization and the performance improvements.
5. After your modifications pass the tests, run `/home/user/primer_tool.py` and redirect its standard output to `/home/user/result.json`.

Ensure your final modifications leave `/home/user/result.json` containing the optimized parameters in the exact JSON format printed by the script, and that `/home/user/profile_baseline.txt` exists.