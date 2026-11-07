"""A small, reproducible workflow for examining categorical signals."""

import math

import pandas as pd

from information.entropy import EntroPy
from utilities.pyutils import as_frame, discretize, discretize_pair


def audit(data, target, reference=None, bins=None):
    """Rank features by empirical shared information and compare marginals.

    No model is trained. Rows within ``data`` are paired observations; reference
    rows are an independent sample. Drift is D_KL(current || reference).
    """
    data = as_frame(data)
    if target not in data.columns:
        raise ValueError(f"target column {target!r} was not found")
    if not all(isinstance(column, str) for column in data.columns):
        raise ValueError("audit column names must be strings")
    prepared = discretize(data, bins)
    target_entropy = EntroPy.shannon_entropy(prepared[[target]])
    features = []
    for column in data:
        if column == target:
            continue
        mi = EntroPy.mutual_information(prepared[[target]], prepared[[column]])
        features.append({
            "feature": column,
            "states": int(prepared[column].nunique()),
            "mutual_information_bits": mi,
            "remaining_uncertainty_bits": max(0.0, target_entropy - mi),
            "fraction_of_target_information": min(1.0, mi / target_entropy) if target_entropy else 0.0,
        })
    features.sort(key=lambda row: (-row["mutual_information_bits"], row["feature"]))
    notes = [
        "These are empirical estimates, not significance tests or evidence of causation.",
        "Feature rankings are individual associations; they do not measure joint interactions or incremental model value.",
    ]
    if target_entropy == 0:
        notes.append("The target is constant: there is no observed target uncertainty to explain.")
    high_cardinality = [column for column in prepared
                        if len(prepared) >= 20 and prepared[column].nunique() / len(prepared) >= 0.2]
    if high_cardinality:
        notes.append("Many distinct states relative to rows in: " + ", ".join(high_cardinality)
                     + ". IDs and sparse samples can inflate empirical mutual information; consider explicit binning for continuous measurements.")
    drift = []
    if reference is not None:
        reference = as_frame(reference)
        missing = [column for column in data if column not in reference]
        if missing:
            raise ValueError("reference is missing columns: " + ", ".join(missing))
        for column in data:
            current, baseline = discretize_pair(data[[column]], reference[[column]], bins)
            kl = EntroPy.relative_entropy(current, baseline)
            ce = EntroPy.cross_entropy(current, baseline)
            drift.append({
                "column": column,
                "kl_bits": kl if math.isfinite(kl) else None,
                "cross_entropy_bits": ce if math.isfinite(ce) else None,
                "status": "finite" if math.isfinite(kl) else "unseen_in_reference",
            })
        drift.sort(key=lambda row: (row["kl_bits"] is not None, -(row["kl_bits"] or 0), row["column"]))
        notes.append("Drift compares each column separately; joint distribution changes can go undetected.")
        if bins is not None:
            notes.append("Drift uses pooled current/reference bin edges; feature ranking uses current-data edges. Compare reports only with consistent discretization.")
    return {
        "schema_version": 1,
        "rows": len(data),
        "reference_rows": len(reference) if reference is not None else None,
        "target": target,
        "bins": bins,
        "units": "bits",
        "target_entropy_bits": target_entropy,
        "features": features,
        "drift": drift,
        "notes": notes,
    }


def demo_data():
    """Balanced factorial example: one perfect, one noisy, two useless signals."""
    rows, baseline = [], []
    for fault in [0, 1]:
        for zone in ["east", "west"]:
            for trial in range(10):
                for _ in range(4):
                    row = {
                        "fault": "fault" if fault else "healthy",
                        "thermal_state": "hot" if fault else "normal",
                        "alarm": "on" if bool(fault) != (trial >= 8) else "off",
                        "zone": zone,
                        "batch": "A",
                    }
                    rows.append(row)
                    baseline.extend([row.copy() for _ in range(1 if fault else 3)])
    return pd.DataFrame(rows), pd.DataFrame(baseline)
