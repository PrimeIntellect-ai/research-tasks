# test_final_state.py

import os
import json
import pytest

def test_pipeline_json():
    pipeline_path = "/home/user/pipeline.json"
    assert os.path.isfile(pipeline_path), f"File not found: {pipeline_path}"

    with open(pipeline_path, 'r') as f:
        try:
            pipeline = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Invalid JSON in {pipeline_path}")

    assert isinstance(pipeline, list), f"Pipeline must be a JSON array in {pipeline_path}"
    assert len(pipeline) >= 2, f"Pipeline must have at least 2 stages in {pipeline_path}"

    # Find $match and $graphLookup stages
    match_stage = None
    graph_lookup_stage = None

    for stage in pipeline:
        if "$match" in stage:
            match_stage = stage["$match"]
        elif "$graphLookup" in stage:
            graph_lookup_stage = stage["$graphLookup"]

    assert match_stage is not None, "Missing $match stage in pipeline"
    assert match_stage.get("package_name") == "gateway-api", "The $match stage must filter by package_name 'gateway-api'"

    assert graph_lookup_stage is not None, "Missing $graphLookup stage in pipeline"
    gl = graph_lookup_stage
    assert gl.get("from") == "packages", "$graphLookup 'from' field must be 'packages'"
    assert gl.get("startWith") == "$depends_on", "$graphLookup 'startWith' field must be '$depends_on'"
    assert gl.get("connectFromField") == "depends_on", "$graphLookup 'connectFromField' field must be 'depends_on'"
    assert gl.get("connectToField") == "package_name", "$graphLookup 'connectToField' field must be 'package_name'"
    assert gl.get("as") == "transitive_dependencies", "$graphLookup 'as' field must be 'transitive_dependencies'"
    assert gl.get("maxDepth") == 5, "$graphLookup 'maxDepth' field must be 5"

def test_index_strategy_json():
    index_path = "/home/user/index_strategy.json"
    assert os.path.isfile(index_path), f"File not found: {index_path}"

    with open(index_path, 'r') as f:
        try:
            idx = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Invalid JSON in {index_path}")

    assert isinstance(idx, dict), f"Index strategy must be a JSON object in {index_path}"
    assert "package_name" in idx, "Index strategy must target the 'package_name' field"
    assert idx["package_name"] in [1, -1], "Index strategy value for 'package_name' must be 1 or -1"

def test_validated_output_json():
    output_path = "/home/user/validated_output.json"
    assert os.path.isfile(output_path), f"File not found: {output_path}. Did you run validate.py?"

    with open(output_path, 'r') as f:
        try:
            out = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Invalid JSON in {output_path}")

    # The mock output is valid according to the schema, so the output should match the mock output
    assert isinstance(out, list), f"Validated output should be a JSON array, got {type(out).__name__}"
    assert len(out) > 0, "Validated output array is empty"

    first_item = out[0]
    assert first_item.get("package_name") == "gateway-api", "Validated output does not match expected mock output content"
    assert "transitive_dependencies" in first_item, "Missing transitive_dependencies in validated output"
    assert len(first_item["transitive_dependencies"]) == 2, "Incorrect number of transitive dependencies in validated output"