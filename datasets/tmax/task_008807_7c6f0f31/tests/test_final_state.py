# test_final_state.py
import os
import tarfile

def test_rca_file_content():
    rca_path = "/home/user/rca.txt"
    assert os.path.exists(rca_path), f"{rca_path} does not exist. Did you create the root cause analysis file?"
    with open(rca_path, "r") as f:
        content = f.read().strip()
    assert content == "format_logs", f"Expected rca.txt to contain exactly 'format_logs', but got '{content}'"

def test_release_tarball_contains_all_modules():
    tarball_path = "/home/user/build_system/out/release.tar.gz"
    assert os.path.exists(tarball_path), f"{tarball_path} does not exist. Did you re-run the build script?"

    expected_modules = [
        "auth_service",
        "payment_gateway",
        "inventory_manager",
        "notification_worker",
        "api_router"
    ]

    with tarfile.open(tarball_path, "r:gz") as tar:
        names = tar.getnames()

        for mod in expected_modules:
            # Depending on tar version, paths might be prefixed with './'
            expected_config_1 = f"{mod}/config.bin"
            expected_config_2 = f"./{mod}/config.bin"
            assert (expected_config_1 in names) or (expected_config_2 in names), \
                f"Module {mod} is missing config.bin in the release tarball. The build script did not process all modules."

            expected_done_1 = f"{mod}/done"
            expected_done_2 = f"./{mod}/done"
            assert (expected_done_1 in names) or (expected_done_2 in names), \
                f"Module {mod} is missing 'done' file in the release tarball."

            expected_log_1 = f"{mod}/filtered.log"
            expected_log_2 = f"./{mod}/filtered.log"
            assert (expected_log_1 in names) or (expected_log_2 in names), \
                f"Module {mod} is missing 'filtered.log' file in the release tarball."