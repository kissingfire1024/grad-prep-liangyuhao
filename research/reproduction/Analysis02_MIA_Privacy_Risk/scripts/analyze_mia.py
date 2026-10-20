
from pathlib import Path
from datetime import datetime
import csv
import hashlib
import json
import math
import os
import tempfile

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.metrics import roc_auc_score, roc_curve

ROOT = Path.home() / "open-unlearning"
OUT = ROOT / "reports/Analysis02_MIA_Privacy_Risk"

MODELS = {
    "Full": "tofu_Llama-3.2-1B-Instruct_full_verified_baseline",
    "GradAscent": "tofu_Llama-3.2-1B-Instruct_forget01_GradAscent_Clean01_eval",
    "GradDiff": "tofu_Llama-3.2-1B-Instruct_forget01_GradDiff_Clean01_eval",
    "SimNPO": "tofu_Llama-3.2-1B-Instruct_forget01_SimNPO_Clean01_eval",
    "RMU": "tofu_Llama-3.2-1B-Instruct_forget01_RMU_Clean01_eval",
}

N_BOOT = 2000
SEED = 20261010

def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def save_csv(path, rows):
    if not rows:
        raise ValueError("不能写入空表")
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

def tpr_at_fpr(labels, scores, max_fpr=0.05):
    # 不做插值：直接取实际经验 ROC 上满足 FPR<=阈值的最大 TPR。
    fpr, tpr, _ = roc_curve(labels, scores)
    return float(np.max(tpr[fpr <= max_fpr]))

def bootstrap_ci(forget, holdout, seed):
    # 分别在两个类别内部有放回抽样，维持类别样本量。
    rng = np.random.default_rng(seed)
    aucs = []
    diagnostics = []

    for _ in range(N_BOOT):
        f = rng.choice(forget, size=len(forget), replace=True)
        h = rng.choice(holdout, size=len(holdout), replace=True)
        labels = np.r_[
            np.zeros(len(f), dtype=int),
            np.ones(len(h), dtype=int),
        ]
        scores = np.r_[f, h]
        auc = roc_auc_score(labels, scores)
        aucs.append(auc)
        diagnostics.append(max(auc, 1.0 - auc))

    return (
        np.percentile(aucs, [2.5, 97.5]).tolist(),
        np.percentile(diagnostics, [2.5, 97.5]).tolist()
    )

def main():
    if OUT.exists():
        raise SystemExit(f"分析目录已存在，拒绝覆盖: {OUT}")

    loaded = {}
    provenance = []

    # 先完成全部输入校验，再创建输出目录。
    for model, directory in MODELS.items():
        path = ROOT / "saves/eval" / directory / "TOFU_EVAL.json"

        if not path.is_file():
            raise SystemExit(f"缺少源文件: {path}")

        data = json.loads(path.read_text(encoding="utf-8"))
        mia = data["mia_min_k"]

        groups = {}
        for group in ["forget", "holdout"]:
            records = mia[group]["value_by_index"]
            expected = {str(i) for i in range(40)}
            if set(records) != expected:
                raise SystemExit(f"{model}/{group}: 样本索引异常")

            values = np.array(
                [records[str(i)]["score"] for i in range(40)],
                dtype=float,
            )

            if not np.all(np.isfinite(values)):
                raise SystemExit(f"{model}/{group}: 存在非有限分数")

            groups[group] = values

        labels = np.r_[
            np.zeros(40, dtype=int),
            np.ones(40, dtype=int)
        ]
        scores = np.r_[groups["forget"], groups["holdout"]]
        calc_auc = roc_auc_score(labels, scores)

        if abs(calc_auc - mia["auc"]) > 1e-10:
            raise SystemExit(
                f"{model}: AUC 复算不一致 "
                f"{calc_auc} != {mia['auc']}"
            )

        loaded[model] = {
            "groups": groups,
            "labels": labels,
            "scores": scores,
            "auc": float(calc_auc),
            "privleak": float(data["privleak"]["agg_value"]),
        }
        provenance.append({
            "model": model,
            "file": str(path),
            "sha256": sha256(path),
            "official_auc": float(mia["auc"]),
        })

    # 在系统临时目录生成，再完整移动到目标位置。
    # 只读原始评估文件。
    with tempfile.TemporaryDirectory(
        prefix="analysis02_",
        dir=str(OUT.parent)
    ) as tmp:
        stage = Path(tmp) / OUT.name
        stage.mkdir()
        tables = stage / "tables"
        figures = stage / "figures"
        tables.mkdir()
        figures.mkdir()

        rows = []
        sample_rows = []

        for i, (model, info) in enumerate(loaded.items()):
            f = info["groups"]["forget"]
            h = info["groups"]["holdout"]
            y = info["labels"]
            s = info["scores"]

            auc = info["auc"]
            reverse = 1.0 - auc
            diagnostic = max(auc, reverse)

            ci, ci_diag = bootstrap_ci(f, h, SEED + i)

            # 官方方向：高分被判为 Holdout。
            official_tpr = tpr_at_fpr(y, s)

            # 成员识别：取负分数，Forget 为正类。
            member_labels = 1 - y
            member_tpr = tpr_at_fpr(member_labels, -s)

            # 反向方向仅作诊断，不作为独立泛化攻击成绩。
            flipped_member_tpr = tpr_at_fpr(member_labels, s)

            rows.append({
                "model": model,
                "n_forget": len(f),
                "n_holdout": len(h),
                "official_auc": auc,
                "official_auc_ci_low": ci[0],
                "official_auc_ci_high": ci[1],
                "reverse_auc": reverse,
                "direction_agnostic_auc": diagnostic,
                "diagnostic_ci_low": ci_diag[0],
                "diagnostic_ci_high": ci_diag[1],
                "tpr_5pct_fpr_official_holdout": official_tpr,
                "tpr_5pct_fpr_member_default": member_tpr,
                "tpr_5pct_fpr_member_flipped": flipped_member_tpr,
                "privleak": info["privleak"],
                "mean_forget_score": float(f.mean()),
                "mean_holdout_score": float(h.mean()),
            })

            for group, values in [("forget", f), ("holdout", h)]:
                for idx, score in enumerate(values):
                    sample_rows.append({
                        "model": model,
                        "group": group,
                        "sample_index": idx,
                        "min_k_score": float(score),
                    })

        save_csv(tables / "MIA_summary.csv", rows)
        save_csv(tables / "MIA_sample_scores.csv", sample_rows)

        # 图1：官方 ROC
        plt.figure(figsize=(8, 6))
        for model, info in loaded.items():
            fpr, tpr, _ = roc_curve(info["labels"], info["scores"])
            plt.plot(
                fpr, tpr,
                label=f"{model} (AUC={info['auc']:.3f})"
            )
        plt.plot([0, 1], [0, 1], "--", alpha=0.5)
        plt.xlabel("False Positive Rate")
        plt.ylabel("True Positive Rate")
        plt.title("Official OpenUnlearning MIA ROC")
        plt.legend(fontsize=9)
        plt.tight_layout()
        plt.savefig(figures / "official_roc.png", dpi=170)
        plt.close()

        # 图2：将 Forget 设为正类的反向 ROC
        plt.figure(figsize=(8, 6))
        for model, info in loaded.items():
            y = 1 - info["labels"]
            s = -info["scores"]
            fpr, tpr, _ = roc_curve(y, s)
            plt.plot(
                fpr, tpr,
                label=f"{model} (AUC={info['auc']:.3f})"
            )
        plt.plot([0, 1], [0, 1], "--", alpha=0.5)
        plt.xlabel("False Positive Rate")
        plt.ylabel("True Positive Rate")
        plt.title("Membership-Oriented ROC (Same Ranking)")
        plt.legend(fontsize=9)
        plt.tight_layout()
        plt.savefig(figures / "membership_roc.png", dpi=170)
        plt.close()

        # 图3：Min-K% 分数分布（每个模型各有一组）
        fig, axes = plt.subplots(
            len(MODELS), 1,
            figsize=(9, 11),
            constrained_layout=True,
        )
        for ax, (model, info) in zip(axes, loaded.items()):
            f = info["groups"]["forget"]
            h = info["groups"]["holdout"]
            ax.hist(f, bins=15, alpha=0.6, label="Forget")
            ax.hist(h, bins=15, alpha=0.6, label="Holdout")
            ax.set_title(model)
            ax.set_xlabel("Min-K% Score")
            ax.legend(fontsize=8)
        fig.savefig(figures / "score_distributions.png", dpi=170)
        plt.close(fig)

        # 图4：官方AUC和方向无关诊断AUC
        names = [r["model"] for r in rows]
        x = np.arange(len(names))
        width = 0.35
        plt.figure(figsize=(9, 5))
        plt.bar(
            x - width / 2,
            [r["official_auc"] for r in rows],
            width,
            label="Official AUC"
        )
        plt.bar(
            x + width / 2,
            [r["direction_agnostic_auc"] for r in rows],
            width,
            label="Direction-Agnostic Diagnostic"
        )
        plt.axhline(0.5, linestyle="--", linewidth=1)
        plt.xticks(x, names)
        plt.ylim(0, 1.05)
        plt.ylabel("ROC-AUC")
        plt.legend()
        plt.title("MIA Ranking Separability")
        plt.tight_layout()
        plt.savefig(figures / "auc_comparison.png", dpi=170)
        plt.close()

        table_lines = [
            "| 模型 | 官方 AUC | 95% CI | 方向无关 AUC | 95% CI |",
            "|---|---:|---:|---:|---:|",
        ]
        for r in rows:
            table_lines.append(
                f"| {r['model']} | {r['official_auc']:.4f} "
                f"| [{r['official_auc_ci_low']:.4f}, "
                f"{r['official_auc_ci_high']:.4f}] "
                f"| {r['direction_agnostic_auc']:.4f} "
                f"| [{r['diagnostic_ci_low']:.4f}, "
                f"{r['diagnostic_ci_high']:.4f}] |"
            )

        report = f"""# Analysis02：MIA 成员推断与隐私风险分析

## 一、分析基本信息

- 创建时间：{datetime.now().isoformat(timespec="seconds")}
- 数据来源：五个模型已保存的 TOFU_EVAL.json
- Forget：40 样本
- Holdout：40 样本
- 攻击方法：OpenUnlearning Min-K% Probability Attack
- 是否使用 GPU：否
- 是否执行新的攻击：否，仅分析已有攻击分数
- Bootstrap：分层重采样 {N_BOOT} 次
- 随机种子：{SEED}

## 二、来源与指标定义

依据本地 OpenUnlearning 源代码：

- `src/evals/metrics/mia/min_k.py`
- `src/evals/metrics/mia/utils.py`
- `src/evals/metrics/privacy.py`

官方将 Forget 标记为 0，Holdout 标记为 1；
使用负的最低 K% Token 对数概率均值作为 Min-K% 分数。

- 官方 AUC：`roc_auc_score(labels, scores)`
- 反向 AUC：`1 - official_auc`
- 方向无关诊断：`max(AUC, 1-AUC)`

方向无关 AUC 是本研究补充的探索性指标，
**不是 OpenUnlearning 官方隐私泄露指标，
也不是经过独立校准的现实攻击成功率。**

## 三、结果

{chr(10).join(table_lines)}

## 四、图表

![官方 ROC](figures/official_roc.png)

![成员方向 ROC](figures/membership_roc.png)

![Min-K 分数分布](figures/score_distributions.png)

![AUC 对比](figures/auc_comparison.png)

## 五、低误报率与隐私解释

低误报率 TPR 采用经验 ROC 上 FPR<=5% 的最大 TPR，
不进行插值。详细数值见 `tables/MIA_summary.csv`。

只有 40 个 Holdout 样本，FPR 步长为 2.5%，
因此不把低 FPR 的 TPR 作为医学隐私保证。

Min-K 分数中的 AUC 低于 0.5 表示发生反向排序，
并不等于攻击者无法区分 Forget 和 Holdout。

对同一批样本事后选择最佳方向会产生评估偏差，
方向无关 AUC 仅作为数据分离的描述性诊断。
后续真实攻击应使用独立校准集确定方向，
再在不重叠的测试集进行验证。

PrivLeak 按 OpenUnlearning 定义为相对参考值变化，
不等于隐私泄露百分比。

## 六、研究局限性

1. TOFU 为虚构人物数据，不构成真实患者隐私实验。
2. 分层 Bootstrap 置信区间反映此样本规模下的抽样不确定性，
   不涵盖不同随机种子、攻击模型或数据分布的变化。
3. 当前 MIA 是一种固定 Min-K% 分数攻击，
   未涵盖更强的自适应成员推断攻击。
4. GradAscent 存在 Model Utility 为零的问题，
   不能单凭 MIA 分数解释为有效隐私保护。
5. 本分析未测试敏感属性推断、患者记录重建或遗忘恢复攻击。

## 七、文件与可复现性

- `tables/MIA_summary.csv`：五模型统计指标
- `tables/MIA_sample_scores.csv`：原始逐样本 Min-K 分数
- `figures/`：四张真实数据绘图
- `scripts/analyze_mia.py`：本次实际分析代码
- `SOURCE_MANIFEST.json`：原始评估文件哈希

原始 Clean 模型、评估文件和封存的 Exp009 保持不变。
"""

        (stage / "实验分析报告.md").write_text(
            report, encoding="utf-8"
        )
        (stage / "SOURCE_MANIFEST.json").write_text(
            json.dumps(provenance, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

        scripts = stage / "scripts"
        scripts.mkdir()

        # 将实际脚本保存在归档中。
        source_script = Path(__file__)
        if source_script.is_file():
            (scripts / "analyze_mia.py").write_bytes(
                source_script.read_bytes()
            )

        os.replace(stage, OUT)

    print("========== Analysis02 完成 ==========")
    for r in rows:
        print(
            f"{r['model']:11s} "
            f"AUC={r['official_auc']:.6f} "
            f"DA-AUC={r['direction_agnostic_auc']:.6f} "
            f"CI=[{r['official_auc_ci_low']:.4f}, "
            f"{r['official_auc_ci_high']:.4f}]"
        )
    print("结果目录:", OUT)

if __name__ == "__main__":
    main()
