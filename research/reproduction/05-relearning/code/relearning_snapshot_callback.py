import os

from transformers import TrainerCallback


class RelearningSnapshotCallback(TrainerCallback):
    """
    Save model/tokenizer snapshots at selected cumulative optimizer steps
    during one continuous relearning trajectory.

    This callback does not modify:
      - loss
      - optimizer
      - LR scheduler
      - gradients
      - training data

    It only saves snapshots.
    """

    def __init__(self, snapshot_steps=(1, 5, 10, 20, 50)):
        self.snapshot_steps = set(snapshot_steps)
        self.processing_class = None

    def on_train_begin(self, args, state, control, **kwargs):
        self.processing_class = kwargs.get("processing_class")

        print(
            f"[RelearningSnapshotCallback] "
            f"snapshot steps = {sorted(self.snapshot_steps)}"
        )

        return control

    def on_step_end(self, args, state, control, **kwargs):
        step = int(state.global_step)

        if step not in self.snapshot_steps:
            return control

        model = kwargs.get("model")

        if model is None:
            raise RuntimeError(
                "RelearningSnapshotCallback did not receive model."
            )

        snapshot_dir = os.path.join(
            args.output_dir,
            f"relearn-step-{step}"
        )

        os.makedirs(snapshot_dir, exist_ok=True)

        print(
            f"\n[RelearningSnapshotCallback] "
            f"Saving step {step} -> {snapshot_dir}"
        )

        model.save_pretrained(snapshot_dir)

        if self.processing_class is not None:
            self.processing_class.save_pretrained(snapshot_dir)

        print(
            f"[RelearningSnapshotCallback] "
            f"Step {step} snapshot saved.\n"
        )

        return control
