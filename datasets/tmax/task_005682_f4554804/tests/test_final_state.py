# test_final_state.py
import os
import math
import re

def compute_expected():
    raw_vals = []
    with open('/home/user/raw_sensor.csv', 'r') as f:
        for line in f:
            parts = line.strip().split(',')
            if len(parts) == 2:
                if parts[1] == 'NaN':
                    raw_vals.append(None)
                else:
                    raw_vals.append(float(parts[1]))

    # 1. Global mean of valid
    valid_vals = [v for v in raw_vals if v is not None]
    global_mean = sum(valid_vals) / len(valid_vals)

    # 2. Replace NaN
    imputed_vals = [v if v is not None else global_mean for v in raw_vals]

    # 3. Cap outliers
    # We will calculate both population and sample std dev to be robust against C++ implementations
    mean_imputed = sum(imputed_vals) / len(imputed_vals)
    variance_pop = sum((v - mean_imputed)**2 for v in imputed_vals) / len(imputed_vals)
    variance_samp = sum((v - mean_imputed)**2 for v in imputed_vals) / (len(imputed_vals) - 1)

    std_dev_pop = math.sqrt(variance_pop)
    std_dev_samp = math.sqrt(variance_samp)

    def get_best_for_std(std_dev):
        upper_bound = mean_imputed + 3 * std_dev
        lower_bound = mean_imputed - 3 * std_dev

        capped_vals = [max(lower_bound, min(upper_bound, v)) for v in imputed_vals]

        ref_vals = []
        with open('/home/user/reference_sensor.csv', 'r') as f:
            for line in f:
                parts = line.strip().split(',')
                if len(parts) == 2:
                    ref_vals.append(float(parts[1]))

        best_w = None
        best_mse = float('inf')

        for w in [1, 3, 5, 7, 9, 11]:
            smoothed = []
            for i in range(len(capped_vals)):
                start = max(0, i - w + 1)
                window = capped_vals[start:i+1]
                smoothed.append(sum(window) / len(window))

            mse = sum((s - r)**2 for s, r in zip(smoothed, ref_vals)) / len(ref_vals)
            if mse < best_mse:
                best_mse = mse
                best_w = w

        return best_w, best_mse

    w_pop, mse_pop = get_best_for_std(std_dev_pop)
    w_samp, mse_samp = get_best_for_std(std_dev_samp)

    return [(w_pop, mse_pop), (w_samp, mse_samp)]

def test_best_param_file():
    param_file = "/home/user/best_param.txt"
    assert os.path.isfile(param_file), f"File {param_file} does not exist. The pipeline did not output the result."

    with open(param_file, 'r') as f:
        content = f.read().strip()

    expected_results = compute_expected()

    # Match format W=X, MSE=Y.YYYY
    match = re.match(r"^W=(\d+),\s*MSE=([\d\.]+)$", content)
    assert match, f"Content of {param_file} does not match the required format 'W=[best_W], MSE=[lowest_MSE_rounded_to_4_decimal_places]'. Found: '{content}'"

    w_val = int(match.group(1))
    mse_val = float(match.group(2))

    valid = False
    for expected_w, expected_mse in expected_results:
        if w_val == expected_w and abs(mse_val - expected_mse) < 0.01:
            valid = True
            break

    assert valid, f"The values W={w_val}, MSE={mse_val} are incorrect. Expected W={expected_results[0][0]}, MSE around {expected_results[0][1]:.4f}."