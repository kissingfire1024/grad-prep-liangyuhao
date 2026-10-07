# Issues — Experiment 002

1. Initial training failed because the WSL proxy was not exported.
2. Proxy setup was added to the reproduction scripts.
3. Evaluation uses batch size 1 because larger batches exceed 12 GB VRAM.
4. SDPA is used instead of FlashAttention2.
5. BF16 NumPy conversion required the existing float().cpu().numpy() evaluation patch.
6. GradDiff showed severe repetitive generation degeneration.
7. Retain99 PrivLeak is not treated as directly comparable because of the retain-log/reference warning.
