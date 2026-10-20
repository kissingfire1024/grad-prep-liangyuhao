# GradAscent Recovery01 Extension — Stage Report V1

## 1. 实验说明

- 方法：GradAscent。
- 起始模型：GradAscent_Clean01。
- Attack：准标识符关联数据微调。
- Control：匹配的无关数据微调。
- Seed=42，Learning Rate=1e-5，训练20步。
- Checkpoint：Step 5、10、15、20。
- TOFU forget01：40条问答，涉及两名虚构人物。
- 身份目标：B0、N20。
- 重要前提：GradAscent Clean01 存在严重效用崩溃。

## 2. 官方 TOFU 评估

| 指标 | Clean01 | Attack20 | Control20 | Attack-Control |
|---|---:|---:|---:|---:|
| Forget QA Probability | 4.355751046e-11 | 0.0007077715301 | 0.01159492731 | -0.01088715578 |
| Forget ROUGE-L Recall | 0 | 0.1876830717 | 0.2214617385 | -0.03377866677 |
| Retain QA Probability | 2.095917096e-08 | 0.09719760895 | 0.3402478027 | -0.2430501938 |
| Retain ROUGE-L Recall | 0.002962596811 | 0.3091997819 | 0.3742493698 | -0.06504958788 |
| Model Utility | 0 | 0.3218475402 | 0.4733395574 | -0.1514920172 |
| Forget Quality | 1.488272292e-21 | 0.5786001417 | 0.4045874057 | +0.174012736 |
| MIA Min-K AUC | 0.16875 | 0.05125 | 0.091875 | -0.040625 |
| Privacy Leakage | 58.14506539 | 80.49940545 | 72.77051128 | +7.728894172 |
| Extraction Strength | 0.02905940823 | 0.02989274157 | 0.03968918399 | -0.009796442427 |

## 3. 逐样本配对结果

| 指标 | 问题组 | 平均A-C | 中位A-C | 正向 | 相等 | 负向 |
|---|---|---:|---:|---:|---:|---:|
| Forget QA Probability | 全部 | -0.0108871558 | -0.0030016080 | 0 | 0 | 40 |
| Forget QA Probability | B0人物组 | -0.0080287324 | -0.0006765574 | 0 | 0 | 20 |
| Forget QA Probability | N20人物组 | -0.0137455791 | -0.0110902786 | 0 | 0 | 20 |
| Forget ROUGE-L | 全部 | -0.0337786668 | -0.0104166667 | 10 | 10 | 20 |
| Forget ROUGE-L | B0人物组 | -0.0272352389 | +0.0000000000 | 7 | 5 | 8 |
| Forget ROUGE-L | N20人物组 | -0.0403220947 | -0.0322580645 | 3 | 5 | 12 |
| Retain ROUGE-L | 全部 | -0.0650495879 | -0.0459830867 | 85 | 71 | 244 |

## 4. 身份恢复结果

| 目标 | Step0命中 | Attack20命中 | Control20命中 | A-C姓名LogP | A-C姓名Margin |
|---|---|---|---|---:|---:|
| B0 | False | False | False | -2.79914117 | +0.40060782 |
| N20 | False | False | False | -3.28616476 | -1.35001755 |

## 5. 实验观察

1. GradAscent Clean01 的 Model Utility 为0，自由生成主要表现为重复符号，属于严重效用崩溃。
2. Attack和Control经过20步微调后，模型生成行为和官方效用指标均出现部分恢复。
3. Control20 的 Model Utility 和 Retain ROUGE 均高于 Attack20。
4. 40/40 Forget QA 的 Attack-Control Probability 均为负差异。
5. 两个身份目标均未出现新的完整姓名生成命中。
6. 模型效用恢复不等于身份知识被定向恢复。

## 6. 局限

- 当前仅有一个随机种子。
- 40条问题仅涉及两名虚构人物，存在组内相关性。
- 模型起始效用崩溃，限制了与其他算法的直接比较。
- 尚不能根据概率变化推断具体知识恢复机制。
- 不得将低身份命中率直接解释为隐私保护更强。

## 7. 来源及 SHA256

| 来源 | 相对路径 | SHA256 |
|---|---|---|
| Clean01 | `saves/eval/tofu_Llama-3.2-1B-Instruct_forget01_GradAscent_Clean01_eval/TOFU_EVAL.json` | `abc16e2f7895aadbf59e8a75e7a5671313be247210aa8452c8a9e4ffac83c11e` |
| Attack | `saves/eval/Recovery01_Extension_GradAscent_Attack_Step20/TOFU_EVAL.json` | `a30e7a9e99f6675af7d3b1614f4c862fb5c7c34a8e9ca5a803d2980c527e3955` |
| Control | `saves/eval/Recovery01_Extension_GradAscent_Control_Step20/TOFU_EVAL.json` | `0cab49508ded605c5b246bbb726ba9cd10c0e3f361835f81efcd834e873c1882` |
| Step0 | `reports/Recovery01_Extension/GradAscent_step0_baseline.json` | `c73d4cf7bcec167dfe4837d81425d547efa4030e163bb2f3dc9c8eb435da5775` |
| Recovery | `reports/Recovery01_Extension/GradAscent_checkpoint_recovery_results.json` | `23d14f65a3a3e5002e05e21014aa029b0b68883f29b2757b095654203564eb79` |
| Protocol | `reports/Recovery01_Extension/EXTENSION_PROTOCOL_V1_FROZEN.json` | `79da6189b916d06fe019021a24a249a013b74cae1178df6efbea65f3dc6a6cd0` |

