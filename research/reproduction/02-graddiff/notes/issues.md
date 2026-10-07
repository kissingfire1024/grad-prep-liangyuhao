# 问题记录 — Experiment 002

1. Initial 训练 失败因为the WSL proxy 为 not exported.
2. Proxy setup 为 added到the reproduction scripts.
3. 评估 uses batch size 1因为larger batches exceed 12 GB VRAM.
4. SDPA 是 used instead 的 FlashAttention2.
5. BF16 NumPy conversion required the existing float().cpu().numpy() 评估 patch.
6. GradDiff showed severe repetitive generation degeneration.
7. Retain99 PrivLeak 是 not treated作为directly comparable因为的 the retain-log/reference 警告.
