You are a DevOps engineer tasked with debugging a migration issue in our metrics aggregation pipeline. 

We are replacing an old legacy C utility (`/app/legacy_calc`) with a new Python script (`/home/user/calc_metrics.py`). Both programs are designed to read a sequence of newline-separated floating-point numbers from standard input and output the mean and sample variance of those numbers.

However, our monitoring system has started flagging "statistical anomalies" and precision warnings. In certain cases, especially when the input values are large but have very small variations, the new Python script outputs drastically incorrect variances (sometimes even negative due to catastrophic cancellation).

Here is the current broken implementation of `/home/user/calc_metrics.py`:

```python
import sys

def process_metrics():
    data = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            data.append(float(line))
            
    if len(data) < 2:
        print("Mean: 0.000000")
        print("Variance: 0.000000")
        return
        
    n = len(data)
    mean = sum(data) / n
    
    # Naive variance calculation
    sum_sq = sum(x**2 for x in data)
    variance = (sum_sq - n * (mean**2)) / (n - 1)
    
    print(f"Mean: {mean:.6f}")
    print(f"Variance: {variance:.6f}")

if __name__ == "__main__":
    process_metrics()
```

The legacy binary (`/app/legacy_calc`) handles these floating-point precision issues flawlessly. Unfortunately, the source code for the legacy binary is lost, and it is a stripped binary. 

Your task:
1. Investigate the statistical anomalies and pinpoint the precision loss in the Python script.
2. Interrogate the behavior of the `/app/legacy_calc` binary using shell tools and test inputs to deduce the stable algorithm it uses.
3. Repair the floating-point precision issue in `/home/user/calc_metrics.py`. 
4. Ensure your repaired Python script's output is **strictly, bit-for-bit identical** to `/app/legacy_calc` for any sequence of floating point inputs.

The output must exactly match this format:
```
Mean: <value_rounded_to_6_decimals>
Variance: <value_rounded_to_6_decimals>
```

You can run your tests in the terminal. The automated verification will test your script against thousands of generated inputs to ensure exact equivalence with the legacy binary.