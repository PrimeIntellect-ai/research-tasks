# test_final_state.py
import json
import os
import math
from collections import defaultdict

def test_validated_regions_output():
    observations_path = "/home/user/observations.jsonl"
    output_path = "/home/user/validated_regions.json"

    assert os.path.exists(output_path), f"Output file {output_path} is missing."

    # Compute expected results from the observations file
    region_temps = defaultdict(list)
    region_sensors = defaultdict(set)

    with open(observations_path, "r") as f:
        for line in f:
            if not line.strip():
                continue
            record = json.loads(line)
            schema = record.get("schema")

            if schema == "v1":
                status = record.get("meta", {}).get("state")
                if status == "active":
                    region = record.get("location", {}).get("biome")
                    temp = record.get("data", {}).get("temp_c")
                    sensor = record.get("meta", {}).get("id")
                    if region and temp is not None and sensor:
                        region_temps[region].append(temp)
                        region_sensors[region].add(sensor)
            elif schema == "v2":
                status = record.get("device_info", {}).get("status")
                if status == "calibrated":
                    region = record.get("geo", {}).get("region_name")
                    temp = record.get("readings", {}).get("temperature", {}).get("value")
                    sensor = record.get("device_info", {}).get("uuid")
                    if region and temp is not None and sensor:
                        region_temps[region].append(temp)
                        region_sensors[region].add(sensor)

    expected_results = {}
    for region in region_temps:
        avg_temp = sum(region_temps[region]) / len(region_temps[region])
        expected_results[region] = {
            "average_temperature": avg_temp,
            "unique_sensor_count": len(region_sensors[region])
        }

    # Load actual results
    with open(output_path, "r") as f:
        try:
            actual_data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {output_path} is not valid JSON."

    assert "results" in actual_data, "Output JSON must contain a 'results' key."
    actual_results_list = actual_data["results"]
    assert isinstance(actual_results_list, list), "'results' must be a list."

    actual_results = {}
    for item in actual_results_list:
        region_name = item.get("region_name")
        assert region_name is not None, "Missing 'region_name' in result item."
        actual_results[region_name] = item

    # Compare expected vs actual
    for region, expected in expected_results.items():
        assert region in actual_results, f"Region '{region}' is missing from the output."
        actual = actual_results[region]

        expected_count = expected["unique_sensor_count"]
        actual_count = actual.get("unique_sensor_count")
        assert actual_count == expected_count, f"Region '{region}' unique_sensor_count mismatch: expected {expected_count}, got {actual_count}."

        expected_temp = expected["average_temperature"]
        actual_temp = actual.get("average_temperature")
        assert actual_temp is not None, f"Region '{region}' missing 'average_temperature'."
        assert math.isclose(actual_temp, expected_temp, rel_tol=1e-3, abs_tol=1e-2), \
            f"Region '{region}' average_temperature mismatch: expected {expected_temp}, got {actual_temp}."

    # Ensure no extra regions
    for region in actual_results:
        assert region in expected_results, f"Unexpected region '{region}' found in the output."