# test_final_state.py

import os
import stat

def test_deployment_accuracy():
    golden_data = {
        "alice": "ENGINEERING",
        "bob": "MARKETING",
        "charlie": "SALES",
        "diana": "ENGINEERING",
        "eve": "HUMAN_RESOURCES",
        "frank": "ENGINEERING",
        "grace": "SALES",
        "heidi": "MARKETING",
        "ivan": "ENGINEERING",
        "judy": "SALES"
    }

    correct = 0
    total = len(golden_data)

    for user, dept in golden_data.items():
        dir_path = f"/home/user/accounts/{user}"
        profile_path = f"{dir_path}/.bash_profile"

        if os.path.isdir(dir_path):
            # Check permissions 750
            st = os.stat(dir_path)
            perms = stat.S_IMODE(st.st_mode)
            if perms == 0o750:
                if os.path.isfile(profile_path):
                    with open(profile_path, 'r') as f:
                        content = f.read().strip()
                    if f'export DEPT="{dept}"' in content:
                        correct += 1

    accuracy = correct / total
    assert accuracy >= 0.85, f"Deployment accuracy is {accuracy}, which is below the threshold of 0.85."