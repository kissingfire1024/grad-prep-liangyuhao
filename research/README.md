<h1 align="center">医学大模型遗忘与去学习 · 论文复现与研究笔记</h1>

<p align="center">
  用可核对的复现进度、可回放的实验记录和可执行的对齐检查，理解每篇论文究竟做了什么、为什么有效、在哪里失效。
</p>

<p align="center">
  <a href="#论文清单">论文清单</a> |
  <a href="#复现进度">复现进度</a> |
  <a href="#研究想法总览">研究想法总览</a> |
</p>

## 复现进度

```text
总进度    5%     已复现 0 / 4 篇
代码完成  0%     主流程可跑通 0 篇
指标对齐   0%     与原论文数值误差 < 2% 的条目
实验记录  0%     含可回放日志与随机种子的条目
```


### 分方向进度

| 方向 | 进度 | 说明 |
| --- | --- | --- |
| 医学 LLM 去学习方法 |  5% | 注意力偏移主线已跑通，公平性去学习仍在数据管线阶段 |
| 医学去学习基准与评测 |  5% | AMNESIA 指标对齐中，REMEDI 多标签协议刚完成拆解 |

## 论文清单

每个条目包含论文链接、复现进度、状态与产出物路径。产出物统一放在 `repro/<paper>/` 下，包含代码、配置、日志与对齐报告。

### 医学 LLM 去学习方法

| 论文 | 复现进度 | 状态 | 产出物 |
| --- | --- | --- | --- |
| [Wisdom is knowing what not to say: Hallucination-free LLMs unlearning via attention shifting](https://arxiv.org/abs/2410.12345) | 10% | 进行中 | `repro/attention-shifting/` |
| [Mitigating algorithmic unfairness arising from forgetfulness of medical records in clinical artificial intelligence](https://arxiv.org/abs/2410.12346) | `████░░░░░░` 40% | 进行中 | `repro/fairness-unlearning/` |

### 医学去学习基准与评测

| 论文 | 复现进度 | 状态 | 产出物 |
| --- | --- | --- | --- |
| [AMNESIA: A Large Scale Medical Unlearning Benchmark Suite with Disease-Informed Analysis](https://arxiv.org/abs/2410.12347) |10% | 进行中 | `repro/amnesia/` |
| [REMEDI: A Benchmark for Retention and Unlearning Evaluation in Multi-label Clinical Disease Inference](https://arxiv.org/abs/2410.12348) | 10% | 进行中 | `repro/remedi/` |

> 论文链接为占位地址，请替换为正式 arXiv 摘要页或会议论文页。

## 研究想法总览

想法按“动机 → 假设 → 依赖 → 验证方式”组织。未标注验证方式的想法不进入实现队列。

| 编号 | 想法 | 动机与假设 | 依赖论文 | 优先级 | 状态 |
| --- | --- | --- | --- | --- | --- |
| I-01 | 去学习强度与幻觉率的联合评测 | 删除越彻底，模型在边界问题上越容易编造，两个指标应同时上报 | [Attention Shifting](https://arxiv.org/abs/2410.12345) | P0 | 进行中 |
| I-02 | 公平性约束下的患者记录遗忘 | 只优化遗忘损失会让少数群体样本被优先删除，需加入群体级保留约束 | [Fairness Unlearning](https://arxiv.org/abs/2410.12346) | P0 | 进行中 |
| I-03 | 疾病感知的遗忘难度分层 | 罕见病与常见病的遗忘难度不同，应作为分层评测维度而非单一均值 | [AMNESIA](https://arxiv.org/abs/2410.12347) | P1 | 待开始 |
| I-04 | 多标签场景下的保留–遗忘权衡曲线 | 单标签的遗忘指标无法刻画标签共现导致的间接泄露 | [REMEDI](https://arxiv.org/abs/2410.12348) | P1 | 待开始 |
| I-05 | 跨基准的遗忘一致性检验 | 同一方法在不同基准上的排名是否稳定，决定结论能否外推 | [AMNESIA](https://arxiv.org/abs/2410.12347)、[REMEDI](https://arxiv.org/abs/2410.12348) | P2 | 待开始 |




