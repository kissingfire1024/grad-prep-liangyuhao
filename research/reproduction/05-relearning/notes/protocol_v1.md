# Experiment 005 — Relearning Attack Protocol v1

## Research Question

After an unlearning method strongly suppresses the target behavior, can the
forgotten knowledge be rapidly recovered through a small amount of subsequent
training?

The purpose is to distinguish:

1. observable forgetting / behavioral suppression
2. resistance to knowledge recovery

This experiment does NOT assume that successful recovery proves a specific
latent-memory mechanism. It measures empirical recoverability.

---

## Stage A — Pilot Method

The first pilot attack will use:

    RMU

Base unlearned checkpoint:

    /home/research/open-unlearning/saves/unlearn/
    tofu_Llama-3.2-1B-Instruct_forget01_RMU_test

Model:

    Llama-3.2-1B-Instruct

Dataset:

    TOFU forget01

Reason for using RMU first:

RMU is a representation-level unlearning baseline already completed in
Experiment 004. It therefore provides a useful first case for testing whether
strong post-unlearning behavioral suppression remains recoverable.

This choice is for the pilot experiment only and is not a claim that RMU is
better or worse than the other baselines.

---

## Stage B — Attack

The attack starts from the already-unlearned RMU checkpoint.

The attacker performs ordinary supervised fine-tuning using forget-set
question-answer training examples.

The attack objective is NOT another unlearning objective.

Conceptually:

    RMU checkpoint
        +
    small amount of forget-data supervised training
        ->
    attacked checkpoint

The experiment asks how quickly previously suppressed target behavior returns.

---

## Stage C — Relearning Checkpoints

Evaluate recovery at:

    step 0
    step 1
    step 5
    step 10
    step 20
    step 50

Step 0 is the original RMU checkpoint from Experiment 004.

No additional training is performed for step 0.

The remaining checkpoints are produced from the same RMU starting checkpoint
under the same relearning configuration.

---

## Stage D — Primary Recovery Metrics

At every checkpoint, record at least:

    Forget Q/A Probability
    Forget Q/A ROUGE
    Extraction Strength
    Model Utility

The main object of analysis is the recovery trajectory rather than only the
final checkpoint.

Example:

    relearning step -> forget metric

This produces a recovery curve.

---

## Stage E — Utility Constraint

Recovery of forget-set performance alone is insufficient.

Model Utility must also be monitored so that apparent recovery can be
distinguished from general model instability or degeneration.

---

## Stage F — Interpretation

If target performance rapidly increases after only a small number of supervised
updates, the correct conclusion is:

    the post-unlearning behavior is empirically recoverable under this
    relearning attack.

This alone does NOT prove:

    the exact forgotten representation was preserved unchanged,
    a specific latent-memory mechanism exists,
    or no genuine parameter-level modification occurred.

Additional representation-level analysis is required for such claims.

Likewise, failure to recover under one attack does NOT prove complete deletion.

It only establishes resistance to the tested attack configuration.

---

## Stage G — Later Extension

After the RMU pilot protocol is validated, apply the same attack protocol to:

    GradAscent
    GradDiff
    SimNPO
    RMU

using matched:

    starting conditions
    relearning data
    optimizer configuration
    learning rate
    number of steps
    evaluation protocol

This will allow comparison of recovery trajectories across unlearning methods.

---

## Stage H — Long-Term Medical Extension

The later clinical version will replace generic TOFU target knowledge with
patient-level records.

A future threat model will test whether:

    same-patient correlated records

can act as a recovery channel after patient-level unlearning.

That medical extension is outside Experiment 005 v1.
