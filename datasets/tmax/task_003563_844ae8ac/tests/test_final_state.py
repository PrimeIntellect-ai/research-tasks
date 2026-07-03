# test_final_state.py
import os

def test_c_program_exists():
    assert os.path.exists("/home/user/generate_config.c"), "C source file /home/user/generate_config.c is missing."
    assert os.path.exists("/home/user/generate_config"), "Compiled executable /home/user/generate_config is missing."
    assert os.access("/home/user/generate_config", os.X_OK), "Executable /home/user/generate_config is not executable."

def test_final_config_accuracy():
    agent_file = "/home/user/final_config.txt"
    assert os.path.exists(agent_file), f"Output file {agent_file} is missing."

    expected_lines = [
        "alias: user201@eng.domain.com",
        "route: 10.5.0.201",
        "alias: user202@hr.domain.com",
        "route: 10.2.0.202",
        "alias: user203@mkt.domain.com",
        "route: 10.3.0.203",
        "alias: user204@it.domain.com",
        "route: 10.9.0.204",
        "alias: user205@eng.domain.com",
        "route: 10.4.0.205",
        "alias: user206@fin.domain.com",
        "route: 10.6.0.206",
        "alias: user207@sales.domain.com",
        "route: 10.3.0.207",
        "alias: user208@rnd.domain.com",
        "route: 10.8.0.208"
    ]

    with open(agent_file, 'r') as f:
        agent_lines = [l.strip() for l in f.readlines() if l.strip()]

    correct = 0
    for el in expected_lines:
        if el in agent_lines:
            correct += 1
            agent_lines.remove(el)

    accuracy = correct / len(expected_lines)
    threshold = 0.85

    assert accuracy >= threshold, f"Accuracy {accuracy:.2f} is below the threshold of {threshold:.2f}. Correct lines: {correct}/{len(expected_lines)}."