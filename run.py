"""One-command local setup and launch: python run.py (Python 3.10+)."""

import argparse
import hashlib
from pathlib import Path
import subprocess
import sys
import venv


def main():
    parser = argparse.ArgumentParser(description="Set up EntroPy in .venv and open its local browser UI.")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--no-browser", action="store_true")
    parser.add_argument("--setup-only", action="store_true", help="install dependencies without starting the server")
    args = parser.parse_args()
    if sys.version_info < (3, 10):
        parser.exit(2, "EntroPy needs Python 3.10 or newer. Python 3.12 is recommended.\n")
    if not 1 <= args.port <= 65535:
        parser.error("port must be between 1 and 65535")
    root = Path(__file__).resolve().parent
    environment = root / ".venv"
    python = environment / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")
    try:
        if not python.exists():
            print("Creating a local Python environment in .venv…", flush=True)
            venv.EnvBuilder(with_pip=True).create(environment)
        fingerprint = hashlib.sha256((root / "pyproject.toml").read_bytes()).hexdigest()
        marker = environment / "entropy-setup.txt"
        if not marker.exists() or marker.read_text().strip() != fingerprint:
            print("Installing EntroPy and its dependencies. First setup needs internet access…", flush=True)
            subprocess.run([str(python), "-m", "pip", "install", "-e", str(root)], check=True)
            marker.write_text(fingerprint + "\n")
        if args.setup_only:
            print("Setup complete. Run python run.py to open EntroPy.")
            return 0
        command = [str(python), "-m", "information", "serve", "--port", str(args.port)]
        if not args.no_browser:
            command.append("--open")
        return subprocess.call(command, cwd=root)
    except KeyboardInterrupt:
        return 0
    except (OSError, subprocess.CalledProcessError) as error:
        print(f"Setup could not finish: {error}\nSee docs/LOCAL_DEMO.md for manual setup.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
