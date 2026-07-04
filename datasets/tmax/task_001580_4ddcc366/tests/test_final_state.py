# test_final_state.py
import math
import socket
import pytest

def get_expected_values(f0, damping, target_error):
    def simulate(dt):
        t_vals = []
        y_vals = []
        t = 0.0
        while t <= 5.0 + 1e-9:
            y = math.exp(-damping * t) * math.sin(2 * math.pi * f0 * t)
            t_vals.append(t)
            y_vals.append(y)
            t += dt

        energy = 0.0
        for i in range(1, len(t_vals)):
            dt_i = t_vals[i] - t_vals[i-1]
            energy += 0.5 * (y_vals[i]**2 + y_vals[i-1]**2) * dt_i

        return t_vals, y_vals, energy

    dt = 0.1
    prev_energy = None

    while True:
        t_vals, y_vals, energy = simulate(dt)
        if prev_energy is not None:
            if abs(energy - prev_energy) < target_error:
                break
        prev_energy = energy
        dt /= 2.0

    N = len(y_vals)
    max_mag = -1.0
    dominant_f = 0.0

    # Exclude DC (k=0) and only consider positive frequencies
    for k in range(1, (N + 1) // 2):
        freq = k / (N * dt)
        real = 0.0
        imag = 0.0
        for n in range(N):
            angle = -2.0 * math.pi * k * n / N
            real += y_vals[n] * math.cos(angle)
            imag += y_vals[n] * math.sin(angle)
        mag = math.sqrt(real**2 + imag**2)
        if mag > max_mag:
            max_mag = mag
            dominant_f = freq

    return dt, energy, dominant_f

def send_request(f0, damping, target_error):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10.0)
        s.connect(("127.0.0.1", 8888))
        req = f"ANALYZE {f0} {damping} {target_error}\n"
        s.sendall(req.encode("utf-8"))
        response = s.recv(1024).decode("utf-8").strip()
        s.close()
        return response
    except Exception as e:
        pytest.fail(f"Failed to communicate with the server: {e}")

@pytest.mark.parametrize("f0, damping, target_error", [
    (2.0, 0.5, 0.01),
    (3.5, 0.1, 0.005),
    (1.0, 1.0, 0.001)
])
def test_server_analysis(f0, damping, target_error):
    expected_dt, expected_energy, expected_freq = get_expected_values(f0, damping, target_error)
    response = send_request(f0, damping, target_error)

    parts = response.split()
    assert len(parts) == 4, f"Expected 4 parts in response, got: '{response}'"
    assert parts[0] == "RESULT", f"Expected response to start with RESULT, got: '{response}'"

    try:
        res_dt = float(parts[1])
        res_energy = float(parts[2])
        res_freq = float(parts[3])
    except ValueError:
        pytest.fail(f"Failed to parse numeric values from response: '{response}'")

    assert math.isclose(res_dt, expected_dt, rel_tol=1e-3), f"Expected dt {expected_dt:.4f}, got {res_dt}"
    assert math.isclose(res_energy, expected_energy, rel_tol=1e-3), f"Expected energy {expected_energy:.4f}, got {res_energy}"
    assert math.isclose(res_freq, expected_freq, rel_tol=1e-2), f"Expected dominant freq {expected_freq:.4f}, got {res_freq}"

    # Check exact formatting (4 decimal places)
    expected_str = f"RESULT {expected_dt:.4f} {expected_energy:.4f} {expected_freq:.4f}"
    assert response == expected_str, f"Response formatting incorrect. Expected '{expected_str}', got '{response}'"