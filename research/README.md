<h1 align="center">医学大模型遗忘与去学习 · 论文复现与研究笔记</h1>

<p align="center">
  用可核对的复现进度、可回放的实验记录和可执行的对齐检查，理解每篇论文究竟做了什么、为什么有效、在哪里失效。
</p>

<p align="center">
  <a href="#论文清单">论文清单</a> |
  <a href="#复现进度">复现进度</a> |
  <a href="#研究想法总览">研究想法总览</a> |
</p>


## 论文清单

每个条目包含论文链接、复现进度、状态与产出物路径。产出物统一放在 `repro/<paper>/` 下，包含代码、配置、日志与对齐报告。

### 医学 LLM 去学习方法

| 论文 |  学习笔记 |复现进度 | 状态 | 产出物 |
| --- | --- | --- | --- | --- |
| [Wisdom is knowing what not to say: Hallucination-free LLMs unlearning via attention shifting](https://arxiv.org/abs/2410.12345) | [笔记](https://github.com/kissingfire1024/grad-prep-liangyuhao/blob/main/research/paper-notes/Wisdom%20is%20Knowing%20What%20not%20to%20Say%3A%20Hallucination-Free%20LLMs%20Unlearning%20via%20Attention%20Shifting.md)|10% | 进行中 | `暂无` |
| [Mitigating algorithmic unfairness arising from forgetfulness of medical records in clinical artificial intelligence](https://www.nature.com/articles/s41467-026-72601-7) |[笔记](https://github.com/kissingfire1024/grad-prep-liangyuhao/blob/main/research/paper-notes/Mitigating%20algorithmic%20unfairness%20arising%20from%20forgetfulness%20of%20medical%20records%20in%20clinical%20artificial%20intelligence.md)|40% | 进行中 | `暂无` |
| [AMNESIA: A Large Scale Medical Unlearning Benchmark Suite with Disease-Informed Analysis](https://arxiv.org/abs/2605.30599) |[笔记](https://github.com/kissingfire1024/grad-prep-liangyuhao/blob/main/research/paper-notes/AMNESIA%20A%20Large%20Scale%20Medical%20Unlearning%20Benchmark%20Suite%20with%20Disease-Informed%20Analysis.md)|10% | 进行中 | `暂无` |
| [REMEDI: A Benchmark for Retention and Unlearning Evaluation in Multi-label Clinical Disease Inference](https://arxiv.org/abs/2606.07141) | [笔记](https://github.com/kissingfire1024/grad-prep-liangyuhao/blob/main/research/paper-notes/REMEDI%20A%20Benchmark%20for%20Retention%20and%20Unlearning%20Evaluation%20in%20Multi-label%20Clinical%20Disease%20Inference.md)|10% | 进行中 | `暂无` |
| [The More Popular, The Harder to Forget: Adaptive Popularity for LLM Unlearning](https://arxiv.org/abs/2608.14229) | [笔记](https://github.com/kissingfire1024/grad-prep-liangyuhao/blob/main/research/paper-notes/The%20More%20Popular%2C%20The%20Harder%20to%20Forget%20Adaptive%20Popularity%20for%20LLM%20Unlearning.md)|10% | 进行中 | `暂无` |
| [ZeroUnlearn: Few-Shot Knowledge Unlearning in Large Language Models](https://arxiv.org/abs/2605.18879) | [笔记](https://github.com/kissingfire1024/grad-prep-liangyuhao/blob/main/research/paper-notes/ZeroUnlearn%20Few-Shot%20Knowledge%20Unlearning%20in%20Large%20Language%20Models.md)|10% | 进行中 | `暂无` |
## 复现进度

```text
总进度    5%     已复现 0 / 4 篇
代码完成  0%     主流程可跑通 0 篇
指标对齐   0%     与原论文数值误差 < 2% 的条目
实验记录  0%     含可回放日志与随机种子的条目
```

## 研究想法总览

想法按“动机 → 假设 → 依赖 → 验证方式”组织。未标注验证方式的想法不进入实现队列。

| 编号 | 想法 | 动机与假设 | 依赖论文 | 优先级 | 状态 |
| --- | --- | --- | --- | --- | --- |
| I-01 | 去学习强度与幻觉率的联合评测 | 删除越彻底，模型在边界问题上越容易编造，两个指标应同时上报 | [Attention Shifting](https://arxiv.org/abs/2410.12345) | P0 | 进行中 |
| I-02 | 公平性约束下的患者记录遗忘 | 只优化遗忘损失会让少数群体样本被优先删除，需加入群体级保留约束 | [Fairness Unlearning](https://arxiv.org/abs/2410.12346) | P0 | 进行中 |
| I-03 | 疾病感知的遗忘难度分层 | 罕见病与常见病的遗忘难度不同，应作为分层评测维度而非单一均值 | [AMNESIA](https://arxiv.org/abs/2410.12347) | P1 | 待开始 |
| I-04 | 多标签场景下的保留–遗忘权衡曲线 | 单标签的遗忘指标无法刻画标签共现导致的间接泄露 | [REMEDI](https://arxiv.org/abs/2410.12348) | P1 | 待开始 |
| I-05 | 跨基准的遗忘一致性检验 | 同一方法在不同基准上的排名是否稳定，决定结论能否外推 | [AMNESIA](https://arxiv.org/abs/2410.12347)、[REMEDI](https://arxiv.org/abs/2410.12348) | P2 | 待开始 |




