# test_final_state.py

import os
import zipfile

def test_converted_configs():
    converted_dir = "/home/user/converted_configs"
    assert os.path.isdir(converted_dir), f"Directory {converted_dir} not found."

    db_conf = os.path.join(converted_dir, "db.conf")
    web_conf = os.path.join(converted_dir, "web.conf")

    assert os.path.isfile(db_conf), "db.conf not found in converted_configs."
    assert os.path.isfile(web_conf), "web.conf not found in converted_configs."

    # Check UTF-8 encoding and content
    try:
        with open(db_conf, "r", encoding="utf-8") as f:
            db_content = f.read()
            assert "Café database" in db_content, "db.conf content is incorrect or corrupted during conversion."
    except UnicodeDecodeError:
        assert False, "db.conf is not valid UTF-8."

    try:
        with open(web_conf, "r", encoding="utf-8") as f:
            web_content = f.read()
            assert "Bienvenue à la page" in web_content, "web.conf content is incorrect or corrupted during conversion."
    except UnicodeDecodeError:
        assert False, "web.conf is not valid UTF-8."

def test_master_zip():
    zip_path = "/home/user/master_configs.zip"
    assert os.path.isfile(zip_path), f"Master zip {zip_path} not found."

    with zipfile.ZipFile(zip_path, "r") as zf:
        names = zf.namelist()
        assert "existing.conf" in names, "existing.conf is missing from master_configs.zip. The zip was likely overwritten instead of appended."
        assert "db.conf" in names, "db.conf not found in master_configs.zip."
        assert "web.conf" in names, "web.conf not found in master_configs.zip."

def test_python_script():
    script_path = "/home/user/update_configs.py"
    assert os.path.isfile(script_path), "update_configs.py script not found."

    with open(script_path, "r", encoding="utf-8") as f:
        content = f.read()
        assert "fcntl.flock" in content, "Python script does not seem to use fcntl.flock."

def test_symlinks():
    latest_dir = "/home/user/latest_configs"
    assert os.path.isdir(latest_dir), f"Directory {latest_dir} not found."

    for filename in ["db.conf", "web.conf"]:
        link_path = os.path.join(latest_dir, filename)
        assert os.path.islink(link_path), f"{link_path} is not a symlink."

        target = os.readlink(link_path)
        expected_target = f"/home/user/converted_configs/{filename}"
        assert target == expected_target, f"Symlink for {filename} does not point to the correct absolute path. Expected {expected_target}, got {target}."