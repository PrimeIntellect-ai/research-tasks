# test_final_state.py
import os
import re

def test_test_results_log():
    log_path = '/home/user/workspace/test_results.log'
    assert os.path.exists(log_path), "test_results.log does not exist"

    with open(log_path, 'r') as f:
        log_contents = f.read()

    assert 'PASS' in log_contents, "Tests did not pass according to test_results.log"
    assert 'TestMigrationProperty' in log_contents, "TestMigrationProperty missing in test_results.log"
    assert 'TestGenerateManifest' in log_contents, "TestGenerateManifest missing in test_results.log"

def test_artifact_go_contents():
    artifact_path = '/home/user/workspace/artifact.go'
    assert os.path.exists(artifact_path), "artifact.go does not exist"

    with open(artifact_path, 'r') as f:
        content = f.read()

    assert 'type ArtifactV2 struct' in content, "ArtifactV2 struct is missing in artifact.go"
    assert 'type Manifest struct' in content, "Manifest struct is missing in artifact.go"
    assert 'func Migrate(' in content, "Migrate function is missing in artifact.go"
    assert 'func GenerateManifest(' in content, "GenerateManifest function is missing in artifact.go"

def test_artifact_test_go_exists():
    test_path = '/home/user/workspace/artifact_test.go'
    assert os.path.exists(test_path), "artifact_test.go does not exist"

    with open(test_path, 'r') as f:
        content = f.read()

    assert 'func TestMigrationProperty(' in content, "TestMigrationProperty function is missing in artifact_test.go"
    assert 'func TestGenerateManifest(' in content, "TestGenerateManifest function is missing in artifact_test.go"