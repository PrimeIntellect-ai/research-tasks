# test_final_state.py
import os
import json
import unicodedata

def compute_expected_report():
    raw_path = "/home/user/raw_logs.jsonl"
    if not os.path.exists(raw_path):
        return []

    valid_logs = []
    with open(raw_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                data = json.loads(line)
                if 'timestamp' not in data or 'service' not in data:
                    continue
                data['message'] = unicodedata.normalize('NFC', data.get('message', ''))
                valid_logs.append(data)
            except json.JSONDecodeError:
                continue

    services = {}
    for log in valid_logs:
        services.setdefault(log['service'], []).append(log)

    for srv, logs in services.items():
        logs.sort(key=lambda x: x['timestamp'])

        for metric in ['response_time_ms', 'cpu_load']:
            valid_pts = [(i, l['timestamp'], l['metrics'].get(metric)) 
                         for i, l in enumerate(logs) 
                         if l.get('metrics', {}).get(metric) is not None]

            for i, l in enumerate(logs):
                if l.get('metrics', {}).get(metric) is None:
                    prior = [p for p in valid_pts if p[0] < i]
                    subseq = [p for p in valid_pts if p[0] > i]

                    if not prior and not subseq:
                        val = 0.0
                    elif not prior:
                        val = subseq[0][2]
                    elif not subseq:
                        val = prior[-1][2]
                    else:
                        t1, v1 = prior[-1][1], prior[-1][2]
                        t2, v2 = subseq[0][1], subseq[0][2]
                        t = l['timestamp']
                        val = v1 + (v2 - v1) * (t - t1) / (t2 - t1)

                    if 'metrics' not in l:
                        l['metrics'] = {}
                    l['metrics'][metric] = val

    all_logs = []
    for srv, logs in services.items():
        for l in logs:
            rt = l['metrics']['response_time_ms']
            cpu = l['metrics']['cpu_load']
            score = (rt * 0.5) + (cpu * 100)
            if '[FATAL]' in l['message']:
                score += 1000
            l['score'] = score
            all_logs.append(l)

    all_logs.sort(key=lambda x: x['score'], reverse=True)
    top_3 = all_logs[:3]

    expected_lines = []
    for l in top_3:
        expected_lines.append(f"[{l['timestamp']}] Service {l['service']} score: {l['score']:.2f} | Msg: {l['message']}")

    return expected_lines

def test_anomaly_report_exists_and_correct():
    report_path = "/home/user/anomaly_report.txt"
    assert os.path.exists(report_path), f"The report file {report_path} was not created."

    expected_lines = compute_expected_report()
    assert len(expected_lines) > 0, "Could not compute expected lines, check if raw_logs.jsonl exists and is valid."

    with open(report_path, 'r', encoding='utf-8') as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert len(actual_lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in the report, but found {len(actual_lines)}."

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, f"Mismatch at line {i+1}.\nExpected: {expected}\nActual:   {actual}"