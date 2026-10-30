#!/usr/bin/env bash
# Run the checks named after the suite and write test-results/<suite>/junit.xml.
#
#   .aidev/run-checks.sh <suite> <step>...
#
# This repository holds API tests and tools that other projects' CI runs
# against a live hived/hivemind node; it has no test suite of its own that can
# run here. Steps, one junit case each:
#
#   compile  python -m py_compile over every .py file in the checkout
#   import   import the packaged modules (validate_response, benchmarks) and
#            jsonsocket with poetry.lock's dependencies. testbase is left out:
#            it imports jsondiff, which pyproject.toml does not declare
#   package  build the wheel with the poetry-core backend (no index) and check
#            it carries validate_response and benchmarks
#   cli      benchmarks/benchmark.py --help and --list (no node needed)
#
# Not run: CI's only job, the manual `Trigger any benchmark`, and every API
# test, which need a live node. See .aidev/README.md.
#
# Runs offline in the image of .aidev/runtime/Dockerfile.
set -uo pipefail
cd "$(dirname "$0")/.." || exit 1
root="$PWD"
suite="${1:?usage: $0 <suite> <step>...}"; shift
out="$root/test-results/$suite"
rm -rf "$out"; mkdir -p "$out"
cases="$out/cases.tsv"; : > "$cases"
export PYTHONPATH="$root${PYTHONPATH:+:$PYTHONPATH}" PYTHONDONTWRITEBYTECODE=1

status=0
step() {
    local name="$1"; shift
    local log="$out/$name.log" t0=$SECONDS rc=0
    echo "== $name" >&2
    ( cd "$root" && "$@" ) > "$log" 2>&1 < /dev/null || rc=$?
    if [ "$rc" -eq 0 ]; then
        printf 'case\t%s\tpass\t%s\t\n' "$name" "$((SECONDS - t0))" >> "$cases"
    else
        status=1; tail -40 "$log" >&2
        printf 'case\t%s\tfail\t%s\texit %s\t%s\n' "$name" "$((SECONDS - t0))" "$rc" "$log" >> "$cases"
    fi
    return "$rc"
}

compile_all() {
    find . \( -path ./.git -o -path ./test-results \) -prune -o -name '*.py' -print0 \
        | xargs -0 -r python -m py_compile
}

import_all() {
    python -c 'import validate_response, benchmarks, jsonsocket; print("imported")'
}

package() {
    local dist="$out/dist"
    python -m pip wheel --no-deps --no-build-isolation --no-index -w "$dist" . \
        && python - "$dist" <<'PY'
import sys, zipfile, glob
wheel, = glob.glob(sys.argv[1] + "/*.whl")
names = zipfile.ZipFile(wheel).namelist()
for pkg in ("validate_response/__init__.py", "benchmarks/benchmark.py"):
    assert pkg in names, "wheel lacks " + pkg
print(wheel, len(names), "files")
PY
}

cli() {
    python benchmarks/benchmark.py --help && python benchmarks/benchmark.py --list
}

for s in "$@"; do
    case "$s" in
        compile) step compile compile_all ;;
        import) step import import_all ;;
        package) step package package ;;
        cli) step cli cli ;;
        *) printf 'case\t%s\tfail\t0\tunknown step\n' "$s" >> "$cases"; status=1 ;;
    esac
done
python .aidev/junit_cases.py "$out/junit.xml" "$suite" "$cases"
exit "$status"
