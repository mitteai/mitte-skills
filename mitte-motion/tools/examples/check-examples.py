#!/usr/bin/env python3
"""Check every example of the tools area.

    python3 SKILLS/tools/examples/check-examples.py [--engine <rexx-engine>] [--ffmpeg …] [--fonts …] [--library …]

1. Every `*.motion.json` here is run through `rexx-engine check` (and `check --variant <v>` for each of its
   variants): it must exit 0 with no error diagnostic; warnings are printed.
2. Every `inputs/motion.<tool>.<name>.json` is validated against the tool's published input schema from
   `registry.json` (the dump `scripts/skills-tools-schemas.py` writes) with `jsonschema` when the module is
   installed (a skipped validation is reported, not failed), and the fields it uses must exist in the schema either way.

Exit 1 on any failure. Defaults: `rexx-engine` on PATH (or `REXX_ENGINE_BIN`), the repo's `fonts/` and `library/`,
`ffmpeg` from `REXX_FFMPEG` or PATH.
"""

import argparse
import json
import os
import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def run_check(engine, doc, variant, extra):
    args = [engine, "check", "--doc", str(doc), "--no-verify-fonts"] + extra
    if variant:
        args += ["--variant", variant]
    p = subprocess.run(args, capture_output=True, text=True, cwd=str(HERE))
    diags, ok = [], None
    for line in p.stdout.splitlines():
        try:
            e = json.loads(line)
        except json.JSONDecodeError:
            continue
        if e.get("event") == "diagnostic":
            diags.append(e)
        elif e.get("event") == "result":
            ok = e.get("data", {}).get("ok")
    return p.returncode, ok, diags, p.stderr.strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--engine", default=os.environ.get("REXX_ENGINE_BIN", "rexx-engine"))
    ap.add_argument("--ffmpeg", default=os.environ.get("REXX_FFMPEG", ""))
    ap.add_argument("--fonts", default=str(ROOT / "fonts"))
    ap.add_argument("--library", default=str(ROOT / "library"))
    a = ap.parse_args()
    extra = ["--fonts", a.fonts, "--library", a.library]
    if a.ffmpeg:
        extra += ["--ffmpeg", a.ffmpeg]
    failed = 0

    for doc in sorted(HERE.glob("*.motion.json")):
        variants = [None] + sorted(json.loads(doc.read_text()).get("variants", {}).keys())
        for v in variants:
            code, ok, diags, err = run_check(a.engine, doc, v, extra)
            errors = [d for d in diags if d.get("severity") == "error"]
            label = f"{doc.name}" + (f" --variant {v}" if v else "")
            if code != 0 or ok is not True or errors:
                failed += 1
                print(f"FAIL {label}: exit {code}, ok={ok}")
                for d in errors or diags:
                    print(f"     {d.get('severity')} {d.get('code')} {d.get('path', '')}: {d.get('message')}")
                if err:
                    print("     stderr: " + err[-400:])
            else:
                warns = [d for d in diags if d.get("severity") != "error"]
                print(f"ok   {label}: {len(warns)} warning(s)/info(s)" + ("" if not warns else ": " + ", ".join(sorted({d['code'] for d in warns}))))

    registry = json.loads((HERE / "registry.json").read_text())
    schemas = {t["name"]: t["input_schema"] for t in registry["tools"]}
    try:
        import jsonschema  # noqa: F401
        have = True
    except ImportError:
        have = False
        print("note: python3 jsonschema is not installed; inputs are checked for unknown fields only")
    for path in sorted((HERE / "inputs").glob("motion.*.json")):
        tool = ".".join(path.name.split(".")[:2])
        schema = schemas.get(tool)
        if schema is None:
            failed += 1
            print(f"FAIL {path.name}: no tool {tool} in registry.json")
            continue
        inp = json.loads(path.read_text())
        unknown = [k for k in inp if k not in schema.get("properties", {})]
        if unknown:
            failed += 1
            print(f"FAIL {path.name}: fields not in the schema: {unknown}")
            continue
        if have:
            try:
                jsonschema.validate(inp, schema)
            except jsonschema.ValidationError as e:
                failed += 1
                print(f"FAIL {path.name}: {e.message} at {'/'.join(str(x) for x in e.path)}")
                continue
        print(f"ok   {path.name}")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
