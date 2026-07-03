# test_final_state.py
import os
import json
import math
import urllib.request
import urllib.error
import pytest

def true_f(x):
    # Based on the ground truth values from the image: A=2.5, B=1.2, C=0.3
    return 2.5 * math.sin(x) + 1.2 * math.cos(x) + 0.3 * (x**2)

def test_server_executable_exists():
    assert os.path.isfile("/home/user/math_service/server"), (
        "The C++ server executable was not found at /home/user/math_service/server. "
        "Make sure you fixed the Makefile and compiled the code successfully."
    )

def test_nginx_config_exists():
    assert os.path.isfile("/home/user/proxy/nginx.conf"), (
        "The Nginx configuration file was not found at /home/user/proxy/nginx.conf."
    )

def test_api_mse_threshold():
    test_points = [0.0, 1.0, 2.5, 3.14, -1.5, 10.0]
    mse = 0.0
    threshold = 0.001

    for x in test_points:
        req = urllib.request.Request('http://127.0.0.1:8080/compute', method='POST')
        req.add_header('Content-Type', 'application/json')
        data = json.dumps({"x": x}).encode('utf-8')

        try:
            response = urllib.request.urlopen(req, data=data, timeout=2)
            response_body = response.read().decode('utf-8')
        except urllib.error.URLError as e:
            pytest.fail(f"Failed to connect to the reverse proxy at 127.0.0.1:8080 for x={x}. Error: {e}. "
                        "Ensure both the C++ server and Nginx proxy are running.")
        except Exception as e:
            pytest.fail(f"Unexpected error when querying the API for x={x}: {e}")

        try:
            result_json = json.loads(response_body)
        except json.JSONDecodeError:
            pytest.fail(f"The API response was not valid JSON: {response_body}")

        assert "result" in result_json, f"The JSON response is missing the 'result' key: {result_json}"

        try:
            predicted = float(result_json["result"])
        except ValueError:
            pytest.fail(f"The 'result' value in the JSON response could not be converted to a float: {result_json['result']}")

        actual = true_f(x)
        mse += (predicted - actual) ** 2

    mse /= len(test_points)

    assert mse < threshold, (
        f"The Mean Squared Error (MSE) of your API's responses is {mse:.6f}, "
        f"which is not below the required threshold of {threshold}. "
        "Check your mathematical formula and extracted coefficients."
    )