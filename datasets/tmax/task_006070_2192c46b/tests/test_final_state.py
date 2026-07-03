# test_final_state.py
import os
import csv

def test_files_exist():
    assert os.path.exists("/home/user/processor.cpp"), "/home/user/processor.cpp does not exist."
    assert os.path.exists("/home/user/sensor_processor"), "/home/user/sensor_processor does not exist."
    assert os.access("/home/user/sensor_processor", os.X_OK), "/home/user/sensor_processor is not executable."

def test_csv_and_logs_computed_from_input():
    input_file = "/home/user/sensor_data.csv"
    assert os.path.exists(input_file), f"{input_file} does not exist."

    buckets = {}
    valid_records = 0
    with open(input_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(',')
            if len(parts) >= 3:
                try:
                    ts = int(parts[0])
                    temp = float(parts[2])
                    bucket = (ts // 60) * 60
                    if bucket not in buckets:
                        buckets[bucket] = []
                    buckets[bucket].append(temp)
                    valid_records += 1
                except ValueError:
                    pass

    sorted_buckets = sorted(buckets.keys())

    expected_stats = []
    prev_mean = None
    anomalies = 0

    for b in sorted_buckets:
        temps = buckets[b]
        mean_val = sum(temps) / len(temps)
        max_val = max(temps)
        min_val = min(temps)

        is_anomaly = 0
        if prev_mean is not None:
            if abs(mean_val - prev_mean) > 5.0:
                is_anomaly = 1
                anomalies += 1

        expected_stats.append({
            'bucket_start': str(b),
            'mean': f"{mean_val:.1f}",
            'max': f"{max_val:.1f}",
            'min': f"{min_val:.1f}",
            'is_anomaly': str(is_anomaly)
        })
        prev_mean = mean_val

    output_file = "/home/user/processed_stats.csv"
    assert os.path.exists(output_file), f"{output_file} does not exist."

    with open(output_file, 'r') as f:
        reader = csv.DictReader(f)
        actual_stats = list(reader)

    assert len(actual_stats) == len(expected_stats), f"Expected {len(expected_stats)} rows in output, got {len(actual_stats)}."

    for actual, expected in zip(actual_stats, expected_stats):
        assert actual.get('bucket_start') == expected['bucket_start'], f"Expected bucket_start {expected['bucket_start']}, got {actual.get('bucket_start')}."
        assert actual.get('mean') == expected['mean'], f"Bucket {expected['bucket_start']}: Expected mean {expected['mean']}, got {actual.get('mean')}."
        assert actual.get('max') == expected['max'], f"Bucket {expected['bucket_start']}: Expected max {expected['max']}, got {actual.get('max')}."
        assert actual.get('min') == expected['min'], f"Bucket {expected['bucket_start']}: Expected min {expected['min']}, got {actual.get('min')}."
        assert actual.get('is_anomaly') == expected['is_anomaly'], f"Bucket {expected['bucket_start']}: Expected is_anomaly {expected['is_anomaly']}, got {actual.get('is_anomaly')}."

    log_file = "/home/user/pipeline.log"
    assert os.path.exists(log_file), f"{log_file} does not exist."

    with open(log_file, 'r') as f:
        log_content = f.read()

    assert "[INFO] Pipeline started" in log_content, "Missing '[INFO] Pipeline started' in log."
    assert f"[INFO] Processed {valid_records} valid records" in log_content, f"Missing '[INFO] Processed {valid_records} valid records' in log."
    assert f"[WARN] Detected {anomalies} anomalies" in log_content, f"Missing '[WARN] Detected {anomalies} anomalies' in log."
    assert "[INFO] Pipeline completed" in log_content, "Missing '[INFO] Pipeline completed' in log."