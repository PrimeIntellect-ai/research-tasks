# test_final_state.py
import os
import tarfile
import stat

def test_generate_artifact_script_fixed_and_executable():
    script_path = '/home/user/mlops/generate_artifact.py'
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_archive_script_exists_and_executable():
    script_path = '/home/user/mlops/archive.sh'
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_result_png_valid():
    png_path = '/home/user/mlops/output/result.png'
    assert os.path.isfile(png_path), f"{png_path} does not exist. Did you run the Python script?"

    # A blank image is usually < 3KB. A valid matplotlib plot is > 5KB.
    size = os.path.getsize(png_path)
    assert size > 5000, f"{png_path} is too small ({size} bytes). The plot might still be blank."

def test_archive_tarball_valid():
    tar_path = '/home/user/archive/artifacts.tar.gz'
    assert os.path.isfile(tar_path), f"{tar_path} does not exist. Did you run the bash script?"

    assert tarfile.is_tarfile(tar_path), f"{tar_path} is not a valid tar file."

    with tarfile.open(tar_path, 'r:gz') as tar:
        names = tar.getnames()

        # Check that result.png is in the tarball
        has_result_png = any(name.endswith('result.png') for name in names)
        assert has_result_png, "result.png is not found in the tarball."

        # Check that there are no absolute paths
        for name in names:
            assert not name.startswith('/'), f"Tarball contains absolute path: {name}"
            assert not name.startswith('home/user'), f"Tarball contains full path hierarchy: {name}"