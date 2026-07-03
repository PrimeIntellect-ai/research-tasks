# test_final_state.py
import os

def test_scripts_exist():
    scripts = [
        "/home/user/clean.sh",
        "/home/user/correlation.sh",
        "/home/user/ci.sh"
    ]
    for script in scripts:
        assert os.path.exists(script), f"Script {script} is missing."

def test_clean_data_csv():
    expected_content = """A,B,C,D
1,2.1,5.5,X
2,4.0,6.1,Y
3,6.2,5.9,Z
4,8.1,4.2,W
-1.5,-3.0,5.0,V
6,11.9,4.8,T
10,20.1,5.2,S"""
    assert os.path.exists("/home/user/clean_data.csv"), "/home/user/clean_data.csv is missing."
    with open("/home/user/clean_data.csv", "r") as f:
        content = f.read().strip()
    assert content == expected_content, "Content of /home/user/clean_data.csv is incorrect."

def test_cor_txt():
    assert os.path.exists("/home/user/cor.txt"), "/home/user/cor.txt is missing."
    with open("/home/user/cor.txt", "r") as f:
        content = f.read().strip()
    assert content == "0.9998", f"Expected correlation to be 0.9998, but got {content}"

def test_ci_txt():
    assert os.path.exists("/home/user/ci.txt"), "/home/user/ci.txt is missing."
    with open("/home/user/ci.txt", "r") as f:
        content = f.read().strip()
    assert content == "5.2429,4.8021,5.6837", f"Expected CI to be 5.2429,4.8021,5.6837, but got {content}"