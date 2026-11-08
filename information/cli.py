"""Command-line entry point for a local signal audit."""

import argparse
import json
from pathlib import Path

import pandas as pd

from information.audit import audit, demo_data


def _positive_int(value):
    value = int(value)
    if value < 1:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return value


def main(argv=None):
    parser = argparse.ArgumentParser(description="Measure uncertainty, useful associations, and marginal distribution drift.")
    commands = parser.add_subparsers(dest="command", required=True)
    browser = commands.add_parser("serve", help="open the local browser workbench")
    browser.add_argument("--port", type=_positive_int, default=8765)
    browser.add_argument("--open", action="store_true", help="open the local URL in your default browser")
    demo = commands.add_parser("demo", help="run a reproducible synthetic sensor audit")
    demo.add_argument("--output", type=Path, default=Path("demo-output"))
    analyze = commands.add_parser("analyze", help="audit observations in a CSV file")
    analyze.add_argument("input", type=Path)
    analyze.add_argument("--target", required=True, help="the outcome column to investigate")
    analyze.add_argument("--reference", type=Path, help="optional earlier sample with the same columns")
    analyze.add_argument("--bins", type=_positive_int, help="equal-width bins for numeric columns; default: discrete values")
    analyze.add_argument("--output", type=Path, default=Path("audit-output"))
    args = parser.parse_args(argv)
    if args.command == "serve":
        from information.web import serve
        try:
            serve(args.port, open_browser=args.open)
        except (OSError, OverflowError) as error:
            parser.exit(2, f"error: {error}\n")
        return 0
    try:
        if args.command == "demo":
            data, reference = demo_data()
            target, bins = "fault", None
        else:
            data = pd.read_csv(args.input)
            reference = pd.read_csv(args.reference) if args.reference else None
            target, bins = args.target, args.bins
        result = audit(data, target, reference, bins)
        from information.graphics import plot_audit

        args.output.mkdir(parents=True, exist_ok=True)
        plot_audit(result, args.output / "signal-audit")
        (args.output / "audit.json").write_text(json.dumps(result, indent=2, allow_nan=False) + "\n", encoding="utf-8")
        if args.command == "demo":
            data.to_csv(args.output / "current.csv", index=False)
            reference.to_csv(args.output / "reference.csv", index=False)
    except (ValueError, TypeError, OSError, pd.errors.ParserError) as error:
        parser.exit(2, f"error: {error}\n")
    print(f"EntroPy | {result['rows']} observations | target: {target}")
    print(f"Target uncertainty: {result['target_entropy_bits']:.4f} bits")
    for row in result["features"]:
        print(f"  {row['feature']}: {row['mutual_information_bits']:.4f} bits shared")
    for note in result["notes"]:
        print(f"Note: {note}")
    print(f"Saved report, SVG, and PNG to {args.output.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
