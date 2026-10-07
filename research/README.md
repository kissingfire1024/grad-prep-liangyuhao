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
| [Wisdom is knowing what not to say: Hallucination-free LLMs unlearning via attention shifting](https://arxiv.org/abs/2410.12345) | [笔记](https://github.com/kissingfire1024/grad-prep-liangyuhao/blob/main/research/paper-notes/Wisdom%20is%20Knowing%20What%20not%20to%20Say%3A%20Hallucination-Free%20LLMs%20Unlearning%20via%20Attention%20Shifting.md)|25% | 进行中 | `/reproduction/01到/reproduction/04` |
| [Mitigating algorithmic unfairness arising from forgetfulness of medical records in clinical artificial intelligence](https://www.nature.com/articles/s41467-026-72601-7) |[笔记](https://github.com/kissingfire1024/grad-prep-liangyuhao/blob/main/research/paper-notes/Mitigating%20algorithmic%20unfairness%20arising%20from%20forgetfulness%20of%20medical%20records%20in%20clinical%20artificial%20intelligence.md)|10% | 进行中 | `/reproduction/02` |
| [AMNESIA: A Large Scale Medical Unlearning Benchmark Suite with Disease-Informed Analysis](https://arxiv.org/abs/2605.30599) |[笔记](https://github.com/kissingfire1024/grad-prep-liangyuhao/blob/main/research/paper-notes/AMNESIA%20A%20Large%20Scale%20Medical%20Unlearning%20Benchmark%20Suite%20with%20Disease-Informed%20Analysis.md)|30% | 进行中 | `/reproduction/01到/reproduction/09` |
| [REMEDI: A Benchmark for Retention and Unlearning Evaluation in Multi-label Clinical Disease Inference](https://arxiv.org/abs/2606.07141) | [笔记](https://github.com/kissingfire1024/grad-prep-liangyuhao/blob/main/research/paper-notes/REMEDI%20A%20Benchmark%20for%20Retention%20and%20Unlearning%20Evaluation%20in%20Multi-label%20Clinical%20Disease%20Inference.md)|10% | 进行中 | `/reproduction/01到/reproduction/09` |
| [The More Popular, The Harder to Forget: Adaptive Popularity for LLM Unlearning](https://arxiv.org/abs/2608.14229) | [笔记](https://github.com/kissingfire1024/grad-prep-liangyuhao/blob/main/research/paper-notes/The%20More%20Popular%2C%20The%20Harder%20to%20Forget%20Adaptive%20Popularity%20for%20LLM%20Unlearning.md)|5% | 进行中 | `/reproduction/06到/reproduction/08` |
| [ZeroUnlearn: Few-Shot Knowledge Unlearning in Large Language Models](https://arxiv.org/abs/2605.18879) | [笔记](https://github.com/kissingfire1024/grad-prep-liangyuhao/blob/main/research/paper-notes/ZeroUnlearn%20Few-Shot%20Knowledge%20Unlearning%20in%20Large%20Language%20Models.md)|5% | 进行中 | `/reproduction/04` |
## 复现进度

```text
总进度    50%     已复现 9.5个基础实验，在基础模型和初始数据集上完成了基础框架验证。
代码完成  50%     主流程可跑通
实验记录  50%     已完成的实验，实验日志已保存，模型参数已冻结。
```

## 研究想法总览

医学大语言模型通过正交，参数提示实现更彻底，性能保留更好的unlearning。




