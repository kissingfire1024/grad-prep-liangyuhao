# EXP009 Source 清单 v2 — 冻结 Record

## 状态

EXP009_SOURCE_MANIFEST_V2_FROZEN

## 已冻结 Artifact

File:

data/source_manifest_v2.json

SHA256:

338fc61c8f5046cfe9e64cabe7dd07de19d3667398e0aa7069e769fb8746a8d6

## Cohort

- Validation 实体: E01-E18
- Discovery 实体 Basil/Nikolai 已排除
- Entities: 18
- Heldout targets: 18
- 证据 记录 per 实体: 5
- Total 证据 记录: 90
- Unique 证据 indices: 90

## 审计 结果

Final source 审计:

- 证据 checked: 90
- Unique 证据: 90
- Automated hard violations: 0
- Semantic review 记录: 61
- Manual semantic 审计: 通过

Semantic-review triggers consisting 仅 的 generic literary terms
(e.g. book/books/novel) 或 award names 为 not treated作为book-title
anchors.

No 已选择 证据 记录 为 found到contain a prohibited 显式
book-title anchor 或 direct birth/出生地 bridge under the frozen
选择 protocol.

## Boundary Cases Retained

Some 记录 contain named awards, generic references到books, or
external literary influences. These 是 not prohibited by the frozen
选择 protocol 和 为 retained.

## Replacement History

source_manifest_v1.json 是 preserved作为the original failed-audit
清单.

source_manifest_v2.json supersedes v1用于全部 正式 EXP009 analyses.

The replacements 为 determined 之前 any EXP009 恢复 训练
or 恢复 result 为 observed.

## Immutability Rule

source_manifest_v2.json MUST NOT be 已修改 之后 this 冻结.

Any future correction requires a new 清单 version 和 an 显式
documented reason.

## Important

This 冻结 applies 仅到SOURCE RECORD SELECTION.

Identity masking / attack-text construction 是 a separate downstream
stage 和 必须 be audited independently 之前 训练.

No EXP009 恢复 result has been used到construct this 清单.
