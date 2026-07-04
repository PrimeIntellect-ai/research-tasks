# test_final_state.py

import os
import re
import stat

def test_malware_fixed_exists_and_executable():
    """Verify that the fixed malware binary exists and is executable."""
    filepath = "/home/user/forensics/malware_fixed"
    assert os.path.isfile(filepath), f"Expected executable at {filepath} is missing."

    st = os.stat(filepath)
    assert bool(st.st_mode & stat.S_IXUSR), f"File {filepath} is not executable."

def test_tls_certificates_exist():
    """Verify that the TLS certificate and private key were generated."""
    cert_path = "/home/user/forensics/c2_cert.pem"
    key_path = "/home/user/forensics/c2_key.pem"

    assert os.path.isfile(cert_path), f"Certificate file {cert_path} is missing."
    assert os.path.isfile(key_path), f"Private key file {key_path} is missing."

def test_run_isolated_script():
    """Verify that the isolation script exists and uses unshare."""
    filepath = "/home/user/forensics/run_isolated.sh"
    assert os.path.isfile(filepath), f"Script {filepath} is missing."

    with open(filepath, "r") as f:
        content = f.read()

    assert "unshare" in content, f"Script {filepath} does not contain the 'unshare' command."

def test_final_evidence_redaction():
    """Verify that the final evidence log exists, has SSNs redacted, and retains other data."""
    filepath = "/home/user/forensics/final_evidence.log"
    assert os.path.isfile(filepath), f"Final evidence log {filepath} is missing."

    with open(filepath, "r") as f:
        content = f.read()

    # Check that original SSNs are gone
    assert "123-45-6789" not in content, "Original SSN '123-45-6789' was not redacted."
    assert "987-65-4321" not in content, "Original SSN '987-65-4321' was not redacted."

    # Check that REDACTED-SSN is present
    assert "REDACTED-SSN" in content, "The string 'REDACTED-SSN' was not found in the output."

    # Check that the rest of the data was preserved
    assert "USER: alice" in content, "Data for 'alice' is missing from the final log."
    assert "USER: bob" in content, "Data for 'bob' is missing from the final log."
    assert "EXTRA_DATA_TO_TRIGGER_OVERFLOW: AAAAA" in content, "Overflow payload data was truncated or missing."
    assert "EXTRA_DATA_TO_TRIGGER_OVERFLOW: BBBBB" in content, "Overflow payload data was truncated or missing."

    # Validate exact SSN regex replacement to ensure no other 9-digit patterns exist
    ssn_pattern = re.compile(r'\b\d{3}-\d{2}-\d{4}\b')
    assert not ssn_pattern.search(content), "Found unredacted SSN patterns in the final log."