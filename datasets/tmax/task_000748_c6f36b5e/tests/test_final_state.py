# test_final_state.py
import os
import subprocess
import random
import string

def generate_random_yaml():
    vms_count = random.randint(0, 10)
    status_choices = ["online", "offline", "maintenance", "booting"]

    yaml_lines = []
    yaml_lines.append("request:")
    yaml_lines.append(f'  path: "/api/{"".join(random.choices(string.ascii_lowercase, k=5))}"')
    yaml_lines.append('  method: "GET"')
    yaml_lines.append("vms:")

    for i in range(vms_count):
        node_id = f"qemu-node-{random.randint(1, 1000)}"
        status = random.choice(status_choices)
        cpu = round(random.uniform(0.0, 100.0), 2)
        yaml_lines.append(f"  - id: \"{node_id}\"")
        yaml_lines.append(f"    status: \"{status}\"")
        yaml_lines.append(f"    cpu: {cpu}")

    if vms_count == 0:
        yaml_lines.append("  []")

    return "\n".join(yaml_lines) + "\n"

def test_fuzz_equivalence():
    agent_script = "/home/user/lb_decision.go"
    oracle_path = "/opt/oracle/lb_decision_oracle"

    assert os.path.isfile(agent_script), f"Agent script {agent_script} does not exist."
    assert os.path.isfile(oracle_path), f"Oracle program {oracle_path} does not exist."

    # Compile the agent script to speed up testing
    agent_bin = "/tmp/lb_decision_agent"
    compile_proc = subprocess.run(["go", "build", "-o", agent_bin, agent_script], capture_output=True, text=True, cwd="/home/user")
    assert compile_proc.returncode == 0, f"Failed to compile {agent_script}:\n{compile_proc.stderr}"

    random.seed(42)

    for i in range(500):
        input_yaml = generate_random_yaml()

        # Run oracle
        oracle_proc = subprocess.run([oracle_path], input=input_yaml, capture_output=True, text=True)
        assert oracle_proc.returncode == 0, f"Oracle failed on input:\n{input_yaml}\nStderr:\n{oracle_proc.stderr}"
        oracle_output = oracle_proc.stdout.strip()

        # Run agent
        agent_proc = subprocess.run([agent_bin], input=input_yaml, capture_output=True, text=True)
        assert agent_proc.returncode == 0, f"Agent program failed on input:\n{input_yaml}\nStderr:\n{agent_proc.stderr}"
        agent_output = agent_proc.stdout.strip()

        assert agent_output == oracle_output, (
            f"Mismatch on iteration {i}.\n"
            f"Input YAML:\n{input_yaml}\n"
            f"Expected (Oracle): {oracle_output}\n"
            f"Got (Agent): {agent_output}"
        )

def test_yaml_fixed():
    with open('/app/vendor/yaml.v3/yaml.go', 'r') as f:
        content = f.read()
    assert 'panic("TODO: implement")' not in content, "The panic perturbation in yaml.go is still present."