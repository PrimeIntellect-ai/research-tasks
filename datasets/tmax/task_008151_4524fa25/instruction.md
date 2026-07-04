I am a researcher running a simulation that aggregates millions of small observational data points. Currently, my results are non-reproducible; every time I run my aggregation, the final test statistic changes slightly due to floating-point reduction order issues, causing my hypothesis test to fluctuate around the significance threshold.

I have a dataset located at `/home/user/raw_data.csv` with columns: `id`, `category` (either 'A' or 'B'), and `value` (highly varying floating-point numbers).

Please help me stabilize my analysis by doing the following:

1. **Observational Data Reshaping**: Read `/home/user/raw_data.csv` and group the `value`s by `category`.
2. **Reproducible Aggregation**: Calculate the exact sum of the `value`s for Category 'A' and Category 'B' in a way that completely eliminates floating-point rounding errors caused by reduction order (hint: standard `sum()` or `numpy.sum()` might not be sufficient if the order of elements varies; look into exact floating-point math functions in Python's standard library).
3. **Statistical Hypothesis Comparison**: Compute the test statistic defined as the exact sum of Category A minus the exact sum of Category B. 
4. **Log the Result**: Write this exact statistic to `/home/user/stat_result.txt`. The file should contain only the number, formatted to exactly 15 decimal places (e.g., `0.123456789012345`).
5. **Experimental Data Visualization**: Create a histogram comparing the distributions of the `value`s for Categories A and B. Save this plot to `/home/user/plot.png`. The plot must be a valid PNG image.

Ensure your code is written in Python. You may need to install standard scientific libraries (like `pandas`, `matplotlib`) using pip.