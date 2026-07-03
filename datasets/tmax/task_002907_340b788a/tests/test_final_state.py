# test_final_state.py
import os
import subprocess
import tempfile
import shutil

def test_archiver_script_validity_and_compression():
    script_path = "/home/user/archiver.sh"
    assert os.path.exists(script_path), f"Script not found at {script_path}"
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable"

    with tempfile.TemporaryDirectory() as temp_dir:
        input_dir = os.path.join(temp_dir, "input")
        os.makedirs(input_dir)
        output_file = os.path.join(temp_dir, "output.arc")

        # Create a 5MB dummy log using base64 so it is compressible
        log_path = os.path.join(input_dir, "system.log")
        subprocess.run(f"base64 /dev/urandom | head -c 5000000 > {log_path}", shell=True, check=True)

        # Copy audio file or generate a dummy one if missing
        wav_path = os.path.join(input_dir, "voicemail.wav")
        if os.path.exists("/app/recording.wav"):
            shutil.copy("/app/recording.wav", wav_path)
        else:
            subprocess.run(
                ["ffmpeg", "-f", "lavfi", "-i", "sine=frequency=1000:duration=60", "-ar", "16000", "-ac", "1", wav_path, "-y"],
                check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )

        # Run the student's script
        result = subprocess.run([script_path, input_dir, output_file], capture_output=True, text=True)
        assert result.returncode == 0, f"Script failed with exit code {result.returncode}\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}"
        assert os.path.exists(output_file), f"Output file {output_file} was not created by the script"

        # Check size threshold
        file_size = os.path.getsize(output_file)
        assert file_size <= 250000, f"Threshold Failed: Archive size {file_size} is greater than the 250000 bytes limit."

        # Verify custom archive format
        with open(output_file, "rb") as f:
            header = f.readline().decode('utf-8', errors='ignore')
            assert header == "MANIFEST\n", f"Missing MANIFEST header. Found: {header.strip()}"

            manifest = []
            while True:
                line_bytes = f.readline()
                assert line_bytes, "Reached EOF before ---DATA--- separator."
                line = line_bytes.decode('utf-8', errors='ignore')

                if line == "---DATA---\n":
                    break

                parts = line.strip().split()
                assert len(parts) == 2, f"Invalid manifest line: {line.strip()}"

                filename, size_str = parts[0], parts[1]
                assert size_str.isdigit(), f"Size in manifest is not an integer: {size_str}"
                manifest.append((filename, int(size_str)))

            current_pos = f.tell()
            f.seek(0, 2) # EOF
            end_pos = f.tell()

            total_expected_binary = sum(size for _, size in manifest)
            actual_binary = end_pos - current_pos

            assert total_expected_binary == actual_binary, (
                f"Payload size mismatch. Manifest expects {total_expected_binary} bytes, "
                f"but found {actual_binary} bytes of binary data."
            )

            expected_files = {"system.log", "voicemail.wav"}
            archived_files = {filename for filename, _ in manifest}
            assert expected_files.issubset(archived_files), f"Manifest is missing expected files. Expected {expected_files}, got {archived_files}"