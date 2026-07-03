apt-get update && apt-get install -y python3 python3-pip python3-venv
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    mkdir -p /home/user/data
    mkdir -p /home/user/pipeline

    # Create virtual environment and install dependencies
    python3 -m venv /home/user/etl_env
    /home/user/etl_env/bin/pip install pandas numpy scikit-learn scipy

    # Generate deterministic data
    cat << 'EOF' > /tmp/generate_data.py
import pandas as pd
import numpy as np

np.random.seed(42)

# Historical data
n_hist = 1000
f1_h = np.random.normal(10, 2, n_hist)
f2_h = np.random.normal(5, 1, n_hist)
f3_h = np.random.normal(20, 5, n_hist)
# Revenue depends on features
rev_h = 3.5 * f1_h + 2.0 * f2_h - 1.5 * f3_h + np.random.normal(0, 3, n_hist)

hist_df = pd.DataFrame({'feature_1': f1_h, 'feature_2': f2_h, 'feature_3': f3_h, 'revenue': rev_h})
hist_df.to_csv('/home/user/data/historical.csv', index=False)

# Batch 01 data (with slight drift)
n_batch = 300
f1_b = np.random.normal(10.5, 2, n_batch)
f2_b = np.random.normal(5.2, 1, n_batch)
f3_b = np.random.normal(19.0, 5, n_batch)
rev_b = 3.5 * f1_b + 2.0 * f2_b - 1.5 * f3_b + np.random.normal(0, 3, n_batch) + 2.0 # Drifted revenue

batch_df = pd.DataFrame({'feature_1': f1_b, 'feature_2': f2_b, 'feature_3': f3_b, 'revenue': rev_b})
batch_df.to_csv('/home/user/data/batch_01.csv', index=False)
EOF

    /home/user/etl_env/bin/python /tmp/generate_data.py

    # Compute expected report
    cat << 'EOF' > /tmp/solve_truth.py
import pandas as pd
import numpy as np
import json
from sklearn.linear_model import Ridge
from sklearn.model_selection import GridSearchCV
import scipy.stats as stats

# Ensure divide by zero error is on
np.seterr(divide='raise')

hist = pd.read_csv('/home/user/data/historical.csv')
batch = pd.read_csv('/home/user/data/batch_01.csv')

# Phase 1
X_train = hist[['feature_1', 'feature_2', 'feature_3']]
y_train = hist['revenue']

param_grid = {'alpha': [0.1, 1.0, 10.0, 100.0]}
grid = GridSearchCV(Ridge(), param_grid, cv=5)
grid.fit(X_train, y_train)

best_alpha = grid.best_params_['alpha']
best_score = grid.best_score_

# Phase 2
new_revenue = batch['revenue']
n = len(new_revenue)
mean = np.mean(new_revenue)
sem = stats.sem(new_revenue)
ci = stats.t.interval(confidence=0.95, df=n-1, loc=mean, scale=sem)

# Phase 3
stat, p_val = stats.ttest_ind(hist['revenue'], batch['revenue'], equal_var=False)
drift = bool(p_val < 0.05)

report = {
    "best_alpha": float(best_alpha),
    "cv_best_score": round(float(best_score), 4),
    "new_revenue_mean_ci": [round(float(ci[0]), 4), round(float(ci[1]), 4)],
    "t_test_p_value": round(float(p_val), 4),
    "data_drift_detected": drift
}

with open('/tmp/expected_report.json', 'w') as f:
    json.dump(report, f)
EOF

    /home/user/etl_env/bin/python /tmp/solve_truth.py

    chmod -R 777 /home/user