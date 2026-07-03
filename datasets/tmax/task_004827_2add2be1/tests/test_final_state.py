# test_final_state.py

import os
import re
import pytest
import pandas as pd

def test_flask_binds_to_localhost():
    app_path = "/app/auth_service/app.py"
    assert os.path.exists(app_path), f"File {app_path} does not exist."

    with open(app_path, "r") as f:
        content = f.read()

    # Check that it doesn't bind to 0.0.0.0
    assert "0.0.0.0" not in content, "Flask app is still bound to 0.0.0.0, exposing it to the network."
    # Check that it binds to 127.0.0.1
    assert "127.0.0.1" in content, "Flask app must be explicitly bound to 127.0.0.1."

def test_flask_enforces_hs256():
    app_path = "/app/auth_service/app.py"
    with open(app_path, "r") as f:
        content = f.read()

    # Verify that algorithms=["HS256"] is used in jwt.decode
    assert re.search(r'algorithms\s*=\s*\[\s*[\'"]HS256[\'"]\s*\]', content) or \
           re.search(r"algorithms\s*=\s*\(\s*['\"]HS256['\"]\s*,\s*\)", content), \
           "Flask app does not enforce the HS256 algorithm in jwt.decode."

def test_nginx_ssl_configuration():
    nginx_path = "/app/nginx/nginx.conf"
    assert os.path.exists(nginx_path), f"File {nginx_path} does not exist."

    with open(nginx_path, "r") as f:
        content = f.read()

    assert "443" in content, "Nginx is not configured to listen on port 443."
    assert "ssl_certificate" in content and "/app/certs/server.crt" in content, "Nginx is missing the SSL certificate configuration."
    assert "ssl_certificate_key" in content and "/app/certs/server.key" in content, "Nginx is missing the SSL certificate key configuration."
    assert "proxy_pass" in content and "127.0.0.1:5000" in content, "Nginx is not proxying to 127.0.0.1:5000."

def test_compromised_users_f1_score():
    pred_path = "/home/user/compromised_users.csv"
    true_path = "/root/ground_truth_compromised.csv"

    assert os.path.exists(pred_path), f"Prediction file {pred_path} does not exist."
    assert os.path.exists(true_path), f"Ground truth file {true_path} does not exist."

    try:
        df_pred = pd.read_csv(pred_path)
        assert 'user_id' in df_pred.columns and 'timestamp' in df_pred.columns, "CSV must contain 'user_id' and 'timestamp' columns."
        pred_set = set(zip(df_pred['user_id'].astype(str), df_pred['timestamp'].astype(str)))
    except Exception as e:
        pytest.fail(f"Failed to read or parse predictions: {e}")

    df_true = pd.read_csv(true_path)
    true_set = set(zip(df_true['user_id'].astype(str), df_true['timestamp'].astype(str)))

    tp = len(pred_set.intersection(true_set))
    fp = len(pred_set - true_set)
    fn = len(true_set - pred_set)

    if tp == 0:
        f1 = 0.0
    else:
        precision = tp / (tp + fp)
        recall = tp / (tp + fn)
        f1 = 2 * (precision * recall) / (precision + recall)

    assert f1 >= 0.98, f"F1 score {f1:.4f} is below the required threshold of 0.98."