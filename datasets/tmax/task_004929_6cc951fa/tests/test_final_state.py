# test_final_state.py
import os
import json
import sqlite3
import pytest

DB_PATH = "/home/user/backup_metadata.db"
REPORT_PATH = "/home/user/backup_report.json"

def get_expected_results():
    if not os.path.exists(DB_PATH):
        pytest.fail(f"Database file missing at {DB_PATH}")

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Compute critical backup id
    c.execute("""
        SELECT parent_id, COUNT(*) as children
        FROM backups
        WHERE parent_id IS NOT NULL
        GROUP BY parent_id
        ORDER BY children DESC, parent_id ASC
        LIMIT 1
    """)
    row = c.fetchone()
    critical_backup_id = row[0] if row else None

    # Compute anomalies
    c.execute("""
        SELECT id, cluster_id, duration_sec, timestamp
        FROM backups
        ORDER BY cluster_id, timestamp
    """)
    rows = c.fetchall()

    from collections import defaultdict
    clusters = defaultdict(list)
    for r in rows:
        clusters[r[1]].append(r)

    anomalies = []
    for cluster, backups in clusters.items():
        for i in range(3, len(backups)):
            prev3 = backups[i-3:i]
            avg = sum(b[2] for b in prev3) / 3.0
            if backups[i][2] > 1.5 * avg:
                anomalies.append({
                    "backup_id": backups[i][0],
                    "cluster_id": cluster,
                    "duration": backups[i][2],
                    "moving_avg": round(avg, 2)
                })

    anomalies.sort(key=lambda x: x["backup_id"])
    conn.close()
    return critical_backup_id, anomalies

def test_report_exists():
    assert os.path.exists(REPORT_PATH), f"Report file missing at {REPORT_PATH}"

def test_report_content():
    assert os.path.exists(REPORT_PATH), f"Report file missing at {REPORT_PATH}"

    with open(REPORT_PATH, 'r') as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("Report file is not valid JSON.")

    expected_critical_id, expected_anomalies = get_expected_results()

    assert "critical_backup_id" in report, "Missing 'critical_backup_id' in report."
    assert report["critical_backup_id"] == expected_critical_id, \
        f"Expected critical_backup_id to be {expected_critical_id}, got {report['critical_backup_id']}."

    assert "anomalies" in report, "Missing 'anomalies' in report."
    assert isinstance(report["anomalies"], list), "'anomalies' should be a list."

    actual_anomalies = report["anomalies"]
    assert len(actual_anomalies) == len(expected_anomalies), \
        f"Expected {len(expected_anomalies)} anomalies, got {len(actual_anomalies)}."

    for actual, expected in zip(actual_anomalies, expected_anomalies):
        assert actual.get("backup_id") == expected["backup_id"], \
            f"Expected backup_id {expected['backup_id']}, got {actual.get('backup_id')}."
        assert actual.get("cluster_id") == expected["cluster_id"], \
            f"Expected cluster_id '{expected['cluster_id']}', got '{actual.get('cluster_id')}'."
        assert actual.get("duration") == expected["duration"], \
            f"Expected duration {expected['duration']}, got {actual.get('duration')}."
        assert actual.get("moving_avg") == expected["moving_avg"], \
            f"Expected moving_avg {expected['moving_avg']}, got {actual.get('moving_avg')}."