# test_final_state.py
import os
import socket
import math
import csv
import pytest

def get_matrix(x, y):
    return [
        [math.cos(x) * (y + 1.0), -math.sin(x) * (y + 1.0), x * y],
        [math.sin(x) * (y + 1.0), math.cos(x) * (y + 1.0), x + y],
        [0.1, 0.2, math.exp(-(x*x + y*y))]
    ]

def mat_vec_mul(M, v):
    return [sum(M[i][j] * v[j] for j in range(3)) for i in range(3)]

def vec_norm(v):
    return math.sqrt(sum(val*val for val in v))

def power_iteration(M, num_iter=1000):
    v = [1.0, 1.0, 1.0]
    for _ in range(num_iter):
        v = mat_vec_mul(M, v)
        norm = vec_norm(v)
        if norm == 0:
            break
        v = [val / norm for val in v]
    Mv = mat_vec_mul(M, v)
    return sum(v[i] * Mv[i] for i in range(3)) / sum(v[i] * v[i] for i in range(3))

def qr_decomposition_r_diag(M):
    a1 = [M[0][0], M[1][0], M[2][0]]
    a2 = [M[0][1], M[1][1], M[2][1]]
    a3 = [M[0][2], M[1][2], M[2][2]]

    def dot(u, v): return sum(x*y for x,y in zip(u,v))
    def proj(u, v): 
        c = dot(u, v) / dot(u, u)
        return [c*x for x in u]
    def sub(u, v): return [x-y for x,y in zip(u,v)]

    u1 = a1
    e1 = [x / vec_norm(u1) for x in u1]

    u2 = sub(a2, proj(e1, a2))
    e2 = [x / vec_norm(u2) for x in u2]

    u3 = sub(sub(a3, proj(e1, a3)), proj(e2, a3))
    e3 = [x / vec_norm(u3) for x in u3]

    r11 = dot(e1, a1)
    r22 = dot(e2, a2)
    r33 = dot(e3, a3)
    return r11, r22, r33

def send_tcp_request(req):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2.0)
            s.connect(("127.0.0.1", 9090))
            s.sendall(req.encode('utf-8'))
            resp = s.recv(1024).decode('utf-8')
            return resp
    except Exception as e:
        pytest.fail(f"TCP request failed for {req.strip()}: {e}")

def test_tcp_eigen():
    test_points = [(0.5, 0.5), (0.0, 0.0), (1.0, 0.2)]
    for x, y in test_points:
        M = get_matrix(x, y)
        expected = power_iteration(M)
        req = f"EIGEN {x} {y}\n"
        resp = send_tcp_request(req).strip()
        try:
            actual = float(resp)
        except ValueError:
            pytest.fail(f"Invalid EIGEN response: {resp}")
        assert abs(actual - expected) < 0.05, f"EIGEN mismatch at {x},{y}: expected ~{expected:.4f}, got {actual:.4f}"

def test_tcp_qr_r():
    test_points = [(0.5, 0.5), (0.0, 0.0), (0.8, 0.1)]
    for x, y in test_points:
        M = get_matrix(x, y)
        expected_r = qr_decomposition_r_diag(M)
        req = f"QR_R {x} {y}\n"
        resp = send_tcp_request(req).strip()
        parts = resp.split()
        assert len(parts) == 3, f"Expected 3 values for QR_R, got {len(parts)} in '{resp}'"
        for i in range(3):
            try:
                actual = float(parts[i])
            except ValueError:
                pytest.fail(f"Invalid QR_R response value: {parts[i]}")
            assert abs(abs(actual) - abs(expected_r[i])) < 0.05, f"QR_R mismatch at {x},{y} index {i}: expected ~{expected_r[i]:.4f}, got {actual:.4f}"

def test_csv_visualization():
    csv_path = "/home/user/eigen_vis.csv"
    assert os.path.exists(csv_path), f"CSV file missing at {csv_path}"

    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        assert header == ['x', 'y', 'eigenvalue'], f"Invalid CSV header: {header}"

        rows = list(reader)
        assert len(rows) == 121, f"Expected 121 rows in CSV, got {len(rows)}"

        # Check a few specific rows to ensure correctness
        for row in rows:
            assert len(row) == 3, f"Invalid row format: {row}"
            x, y, eigen = float(row[0]), float(row[1]), float(row[2])

            # Verify grid bounds
            assert 0.0 <= x <= 1.0, f"x value out of bounds: {x}"
            assert 0.0 <= y <= 1.0, f"y value out of bounds: {y}"

            # Spot check (0.0, 0.0)
            if abs(x) < 1e-4 and abs(y) < 1e-4:
                M = get_matrix(x, y)
                expected = power_iteration(M)
                assert abs(eigen - expected) < 0.05, f"CSV Eigenvalue mismatch at {x},{y}: expected ~{expected:.4f}, got {eigen:.4f}"