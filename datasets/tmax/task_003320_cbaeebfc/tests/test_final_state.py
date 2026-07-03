# test_final_state.py
import os
import re

def test_router_fstab():
    fstab_path = "/home/user/router_fstab"
    assert os.path.isfile(fstab_path), f"File {fstab_path} is missing."

    with open(fstab_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip() and not line.strip().startswith('#')]

    assert len(lines) == 1, f"Expected exactly one valid fstab entry, found {len(lines)}."

    fields = lines[0].split()
    assert len(fields) >= 4, "fstab entry must have at least 4 fields (fs_spec, fs_file, fs_vfstype, fs_mntops)."

    fs_spec, fs_file, fs_vfstype, fs_mntops = fields[:4]

    assert fs_spec == "/app/router_fs.ext4", f"Expected fs_spec to be /app/router_fs.ext4, got {fs_spec}"
    assert fs_file == "/mnt/router", f"Expected fs_file to be /mnt/router, got {fs_file}"

    mntops = fs_mntops.split(',')
    assert 'loop' in mntops, "fstab mount options must include 'loop'"
    assert 'ro' in mntops, "fstab mount options must include 'ro'"
    assert 'user' in mntops or 'users' in mntops, "fstab mount options must include 'user' or 'users'"

def test_down_frames_f1_score():
    pred_file = "/home/user/down_frames.txt"
    assert os.path.isfile(pred_file), f"File {pred_file} is missing."

    try:
        with open(pred_file, 'r') as f:
            preds = set(int(line.strip()) for line in f if line.strip().isdigit())
    except Exception as e:
        assert False, f"Error reading {pred_file}: {e}"

    ground_truth = list(range(45, 86)) + list(range(160, 211)) + list(range(260, 281))
    true_set = set(ground_truth)

    tp = len(preds.intersection(true_set))
    fp = len(preds - true_set)
    fn = len(true_set - preds)

    if tp == 0:
        f1 = 0.0
    else:
        precision = tp / (tp + fp)
        recall = tp / (tp + fn)
        f1 = 2 * (precision * recall) / (precision + recall)

    assert f1 >= 0.95, f"F1 Score is {f1:.4f}, which is below the threshold of 0.95."

def test_nginx_config():
    conf_path = "/home/user/lb.conf"
    assert os.path.isfile(conf_path), f"File {conf_path} is missing."

    with open(conf_path, 'r') as f:
        content = f.read()

    # Check daemon off
    assert re.search(r'daemon\s+off\s*;', content), "Nginx config missing 'daemon off;'"

    # Check pid file
    assert re.search(r'pid\s+/home/user/nginx\.pid\s*;', content), "Nginx config missing 'pid /home/user/nginx.pid;'"

    # Check error_log
    assert re.search(r'error_log\s+/home/user/error\.log\s*;', content), "Nginx config missing 'error_log /home/user/error.log;'"

    # Check listen
    assert re.search(r'listen\s+127\.0\.0\.1:8080\s*;', content), "Nginx config missing 'listen 127.0.0.1:8080;'"

    # Check upstream servers
    assert re.search(r'server\s+127\.0\.0\.1:9001\s*;', content), "Nginx config missing backend server 127.0.0.1:9001"
    assert re.search(r'server\s+127\.0\.0\.1:9002\s*;', content), "Nginx config missing backend server 127.0.0.1:9002"
    assert re.search(r'server\s+127\.0\.0\.1:9003\s*;', content), "Nginx config missing backend server 127.0.0.1:9003"

    # Check proxy_pass
    assert re.search(r'proxy_pass\s+http://', content), "Nginx config missing proxy_pass directive to load balance"