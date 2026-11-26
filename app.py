import argparse
import json
import sys
from pathlib import Path
from model import analyze


def main():
    parser = argparse.ArgumentParser(description=analyze.__module__)
    parser.add_argument("input",type=Path,help="Path to a JSON scenario")
    args = parser.parse_args()
    try:
        data = json.loads(args.input.read_text(encoding="utf-8"))
        if not isinstance(data,dict):
            raise ValueError("Expected a JSON object.")
        result = analyze(data)
    except (OSError,ValueError,KeyError) as exc:
        print(f"Input error: {exc}",file=sys.stderr)
        return 2
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
