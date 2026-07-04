# test_final_state.py
import os
import tarfile

def test_release_docs_tar_exists():
    """Verify that the final release archive exists."""
    release_path = '/home/user/release_docs.tar'
    assert os.path.isfile(release_path), f"The target output file {release_path} is missing."

def test_release_docs_tar_contents():
    """Verify that the release archive contains exactly the expected renamed files at the root level."""
    release_path = '/home/user/release_docs.tar'
    assert os.path.isfile(release_path), f"Cannot check contents, {release_path} does not exist."

    expected_files = {
        '01_Introduction.md',
        '02_API_Reference.md',
        '03_Changelog.md'
    }

    try:
        with tarfile.open(release_path, 'r') as tar:
            members = tar.getmembers()

            actual_files = set()
            for member in members:
                # Ensure no directories are included
                assert member.isfile(), f"Archive contains non-file member: {member.name}. It should only contain files."
                # Ensure files are at the root level (no slashes in the path)
                assert '/' not in member.name, f"File {member.name} is not at the root level of the archive."
                actual_files.add(member.name)

            assert actual_files == expected_files, (
                f"Archive contents do not match exactly.\n"
                f"Expected: {expected_files}\n"
                f"Actual: {actual_files}"
            )
    except tarfile.ReadError:
        assert False, f"The file {release_path} is not a valid tar archive."