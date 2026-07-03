# test_final_state.py
import os
import tarfile

def test_converter_c_exists():
    path = '/home/user/converter.c'
    assert os.path.isfile(path), f"Expected C program {path} does not exist."

def test_dataset_csv_content():
    path = '/home/user/dataset.csv'
    assert os.path.isfile(path), f"Expected file {path} does not exist."

    expected_content = (
        "1,100.00\n"
        "3,7.78\n"
        "4,1.23\n"
        "8,42.12\n"
        "10,15.23\n"
        "12,3.14\n"
        "22,5.55\n"
        "25,12.34\n"
        "105,88.88\n"
    )

    with open(path, 'r') as f:
        content = f.read()

    # Ignore trailing newlines for comparison robustness
    assert content.strip() == expected_content.strip(), f"Content of {path} does not match the expected sorted and filtered output."

def test_clean_dataset_archive():
    archive_path = '/home/user/clean_dataset.tar.gz'
    assert os.path.isfile(archive_path), f"Expected archive {archive_path} does not exist."
    assert tarfile.is_tarfile(archive_path), f"File {archive_path} is not a valid tar archive."

    with tarfile.open(archive_path, 'r:gz') as tar:
        members = tar.getnames()
        # The file can be stored as 'dataset.csv' or 'home/user/dataset.csv' depending on how it was archived.
        # We just check if dataset.csv is in any of the paths.
        csv_members = [m for m in members if m.endswith('dataset.csv')]
        assert csv_members, f"dataset.csv not found in {archive_path}"

        # Check content of the archived file
        member_name = csv_members[0]
        f = tar.extractfile(member_name)
        assert f is not None, f"Could not extract {member_name} from {archive_path}"
        content = f.read().decode('utf-8')

        expected_content = (
            "1,100.00\n"
            "3,7.78\n"
            "4,1.23\n"
            "8,42.12\n"
            "10,15.23\n"
            "12,3.14\n"
            "22,5.55\n"
            "25,12.34\n"
            "105,88.88\n"
        )

        assert content.strip() == expected_content.strip(), f"Content of archived dataset.csv does not match the expected output."