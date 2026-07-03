# test_final_state.py

import os
import numpy as np
import pytest
from skimage.metrics import structural_similarity as ssim
from PIL import Image
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def generate_reference_embeddings(eval_txt_path):
    with open(eval_txt_path, 'r') as f:
        lines = [line.strip('\n') for line in f]

    trigrams = set()
    for line in lines:
        for i in range(len(line) - 2):
            trigrams.add(line[i:i+3])

    vocab = sorted(list(trigrams))
    vocab_size = len(vocab)
    vocab_idx = {tg: i for i, tg in enumerate(vocab)}

    N = len(lines)
    counts = np.zeros((N, vocab_size), dtype=np.float32)
    for i, line in enumerate(lines):
        for j in range(len(line) - 2):
            tg = line[j:j+3]
            counts[i, vocab_idx[tg]] += 1.0

    rng = np.random.RandomState(42)
    proj = rng.randn(vocab_size, 64).astype(np.float32)

    embeds = np.dot(counts, proj)
    return embeds

def test_python_embeds_mse():
    eval_txt_path = "/home/user/data/eval.txt"
    python_embeds_path = "/home/user/data/python_embeds.bin"

    assert os.path.exists(python_embeds_path), f"Agent did not create {python_embeds_path}"

    ref_embeds = generate_reference_embeddings(eval_txt_path)
    agent_embeds = np.fromfile(python_embeds_path, dtype=np.float32)

    assert agent_embeds.shape == ref_embeds.flatten().shape, "Agent embeddings shape mismatch"

    mse = np.mean((ref_embeds.flatten() - agent_embeds) ** 2)
    assert mse < 1e-5, f"MSE between python_embeds.bin and reference is {mse}, which is >= 1e-5 threshold."

def test_residual_plot_ssim(tmp_path):
    eval_txt_path = "/home/user/data/eval.txt"
    python_embeds_path = "/home/user/data/python_embeds.bin"
    agent_plot_path = "/home/user/residual_plot.png"

    assert os.path.exists(agent_plot_path), f"Agent did not create {agent_plot_path}"

    ref_embeds = generate_reference_embeddings(eval_txt_path)

    if os.path.exists(python_embeds_path):
        agent_embeds = np.fromfile(python_embeds_path, dtype=np.float32)
    else:
        agent_embeds = np.zeros_like(ref_embeds.flatten())

    # Generate reference plot
    ref_plot_path = tmp_path / "ref_plot.png"

    residuals = ref_embeds.flatten() - agent_embeds

    plt.figure()
    plt.scatter(range(len(residuals)), residuals, alpha=0.5)
    plt.title("Embedding Residuals")
    plt.xlabel("Dimension Index")
    plt.ylabel("Error")
    plt.savefig(ref_plot_path)
    plt.close()

    # Compute SSIM
    img_agent = np.array(Image.open(agent_plot_path).convert('L'))
    img_ref = np.array(Image.open(ref_plot_path).convert('L'))

    if img_agent.shape != img_ref.shape:
        img_agent = np.array(Image.open(agent_plot_path).convert('L').resize(img_ref.shape[::-1]))

    score, _ = ssim(img_ref, img_agent, full=True, data_range=255)
    assert score >= 0.95, f"SSIM between generated plot and reference is {score:.4f}, expected >= 0.95"